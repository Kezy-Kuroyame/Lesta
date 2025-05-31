import os
import time

import chardet
import math
from collections import defaultdict
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import TextFileForm
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

from system.metrics import metrics

from .models import ProcessedFile


def detect_encoding(file):
    """Определение кодировки файла"""
    raw_data = file.read(1024)
    file.seek(0)
    result = chardet.detect(raw_data)
    return result['encoding']


def calculate_tf_idf(all_documents_words):
    """Расчет TF-IDF для всех документов"""
    document_freq = defaultdict(int)
    total_documents = len(all_documents_words)
    all_tf_data = []

    for doc_words in all_documents_words:
        tf_dict = defaultdict(int)
        for word in doc_words:
            tf_dict[word] += 1

        max_tf = max(tf_dict.values()) if tf_dict else 1
        normalized_tf = {word: count / max_tf for word, count in tf_dict.items()}
        all_tf_data.append(normalized_tf)

        for word in set(doc_words):
            document_freq[word] += 1

    idf_dict = {word: math.log10(total_documents / df) for word, df in document_freq.items()}
    return all_tf_data, idf_dict


def clear_temp_uploads():
    """Удаляет все файлы из папки temp_uploads."""
    temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp_uploads')
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении {file_path}: {e}")


def analyze_text(request):
    if request.method == 'GET':
        request.session['uploaded_files'] = []
        clear_temp_uploads()

    if request.method == 'POST':
        form = TextFileForm(request.POST, request.FILES)
        if 'delete_file' in request.POST:
            return handle_file_delete(request)
        elif 'analyze_all' in request.POST:
            return handle_file_analysis(request)
        elif form.is_valid():
            return handle_file_upload(request, form)


    form = TextFileForm()
    return render(request, 'analyzer/analyze.html', {'form': form})

def handle_file_delete(request):
    file_index = int(request.POST.get('delete_file'))
    uploaded_files = request.session.get('uploaded_files', [])

    if 0 <= file_index < len(uploaded_files):
        try:
            os.remove(uploaded_files[file_index]['path'])
        except OSError as e:
            print(f"Ошибка удаления файла: {e}")

        del uploaded_files[file_index]
        request.session['uploaded_files'] = uploaded_files

    return render(request, 'analyzer/analyze.html', {
        'form': TextFileForm(),
        'uploaded_files': uploaded_files
    })


def handle_file_upload(request, form):
    uploaded_files = request.session.get('uploaded_files', [])
    fs = FileSystemStorage(location='temp_uploads')

    for uploaded_file in request.FILES.getlist('text_files'):
        if len(uploaded_files) >= 10:
            break

        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_files.append({
            'name': uploaded_file.name,
            'path': fs.path(filename)
        })
    request.session['uploaded_files'] = uploaded_files
    return render(request, 'analyzer/analyze.html', {
        'form': TextFileForm(),
        'uploaded_files': uploaded_files
    })


def handle_file_analysis(request):
    if 'uploaded_files' not in request.session:
        return render(request, 'analyzer/analyze.html', {
            'form': TextFileForm(),
            'error': 'Нет загруженных файлов для анализа'
        })

    files = request.session['uploaded_files']
    print('files', files)
    if len(files) < 2:
        return render(request, 'analyzer/analyze.html', {
            'form': TextFileForm(),
            'uploaded_files': files,
            'error': 'Необходимо загрузить минимум 2 файла'
        })

    try:
        all_documents_words = []
        for file_info in files:
            start_time = time.time()

            with open(file_info['path'], 'rb') as f:
                encoding = detect_encoding(f)
                content = f.read().decode(encoding)
                words = content.lower().split()
                words = [word.strip('.,!?;:"\'()[]{}') for word in words if word.strip('.,!?;:"\'()[]{}')]
                all_documents_words.append(words)

            end_time = time.time()
            processing_time = end_time - start_time

            # 3) Инкрементим метрику в памяти
            metrics.increment_files_processed()

            # 4) Сохраняем запись в БД
            ProcessedFile.objects.create(
                filename=file_info['name'],
                processing_time=round(processing_time, 5)
            )
        print(metrics.get_metrics())
        all_tf_data, idf_dict = calculate_tf_idf(all_documents_words)

        all_results = []
        for tf_dict, file_info in zip(all_tf_data, files):
            results = [{
                'word': word,
                'tf': tf_dict[word],
                'idf': idf_dict.get(word, 0)
            } for word in tf_dict]

            results.sort(key=lambda x: x['idf'], reverse=True)
            all_results.append({
                'filename': file_info['name'],
                'results': results[:50]
            })

        request.session['analysis_results'] = all_results
        request.session['filenames'] = [f['name'] for f in files]
        request.session.modified = True
        print(reverse('results'))
        print("Данные в сессии перед редиректом:", request.session.keys())
        return redirect(reverse('results'))

    except Exception as e:
        return render(request, 'analyzer/analyze.html', {
            'form': TextFileForm(),
            'uploaded_files': files,
            'error': f'Ошибка анализа: {str(e)}'
        })

def handle_get_request(request):
    form = TextFileForm()
    all_results = request.session.get('analysis_results', [])

    if not request.GET:
        request.session['filtered_results'] = all_results
    else:
        min_idf = request.GET.get('min_idf', None)
        search_query = request.GET.get('search', '')

        filtered_results = []
        for result in all_results:
            filtered_items = [
                item for item in result.get('results', [])
                if (not min_idf or float(item['idf']) >= float(min_idf)) and
                   (not search_query or search_query.lower() in item['word'].lower())
            ]
            if filtered_items:
                filtered_results.append({'filename': result['filename'], 'results': filtered_items})

        request.session['filtered_results'] = filtered_results

    data = request.session.get('filtered_results', all_results)

    # Создаём пагинацию отдельно для каждого файла
    paginated_data = {}
    all_words = []
    for file_data in data:
        words = file_data['results']
        paginator = Paginator(words, 10)
        page_number = request.GET.get(f'page_{file_data["filename"]}', 1)
        page_obj = paginator.get_page(page_number)
        paginated_data[file_data['filename']] = page_obj

        # Добавляем все слова в общий список
        all_words.extend(words)

    # Отбираем топ-10 слов по IDF
    top_words = sorted(all_words, key=lambda x: x['idf'], reverse=True)[:10]
    chart_labels = [word['word'] for word in top_words]
    chart_data = [word['idf'] for word in top_words]

    return render(request, 'analyzer/results.html', {
        'form': form,
        'paginated_data': paginated_data,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'filenames': request.session.get('filenames', [])
    })

