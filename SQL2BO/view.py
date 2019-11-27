from django.shortcuts import render
from django.http.response import HttpResponse
import json
import re

type_dict = {
        'VARCHAR': 'String',
        'CHARACTER': 'String',
        'DECIMAL': 'float',
        'timesatmp': 'Date'
    }
regex = re.compile('\s+')
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'sql2bo.html', context)

def return_post(request):
    ctx ={}
    if request.POST:
        content = request.POST['content']
        print(content)
        res = ""
        try:
            res = sql2bo(content)
        except:
            res = "error"
        finally:
            print('end')
        ctx['result'] = res
        ctx['status'] = 1
    return HttpResponse(json.dumps(ctx))

def sql2bo(txt):
    txt = txt.strip().split('\n')
    lines = list(map(lambda line:regex.split(line[:-1]) if ',' in line else regex.split(line),txt))
    # print(lines)
    select_sent = ",\n".join([line[0] for line in lines])
    # print(select_sent)
    bo = generate_bo(lines)
    return bo+"\n\nselect:\n "+select_sent
    

def generate_bo(lines):
    res = ""
    for line in lines:
        _type = ""
        if '(' in line[1]:
            _type = type_dict[line[1].split('(')[0].strip().upper()] if line[1].split('(')[0].strip().upper() in type_dict else 'String'
        else:
            _type = type_dict[line[1].strip().upper()] if line[1].strip().upper() in type_dict else 'String'
        # print(_type)
        _content_list = line[0].split('_')
        _content = _content_list[0].lower()
        if len(_content_list) > 1:
            for c in _content_list[1:]:
                _content += c.capitalize()
        res += 'private ' + _type + ' ' +_content + ";\n"
        # print(res)
    return res
# def test():
#     txt = """
#     a     decimal,
# b varchar
#     """
#     sql2bo(txt)

# test()