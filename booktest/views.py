from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
# 1.定义视图函数index，必须要返回一个 HttpRequest 对象
# 2.然后去进行url配置，建立url地址和视图的对应关系
# 想让用户输入 http://127.0.0.1:8000/总路由+子路由 时可以显示下面的内容
def index(request):
    "进行处理，和M和T进行交互"
    #
    """
        之前是直接返回的内容:
    text = "<div style='color:hotpink; width:300px; height:300px; background: orange'>Hello world</div>"
    return HttpResponse(text)
    """
    # 现在是要读取模板中的内容来返回
    """
    这是视频1.8版本的原理讲解，在3.2版本这会报错的，所以还是直接使用系统提供的render()渲染吧
    导包 from django.template import loader, RequestContext
    # 1.加载模板文件，
    temp = loader.get_template("booktest/index.html")  # 注意路径
    # 2.定义模板上下文，给模板传递数据，没有的话可以传一个 空字典
    context = RequestContext(request, {})   # 要用RequestContext这个类对象
    # 3.模板渲染
    res_html = temp.render(context)
    return HttpResponse(res_html)
    """
    replace_data = dict(
        my_content="这是替换的第一个参数",
        my_list=list(range(10))
    )
    # 不用替换数据就不用传第三个参数,可以为空
    return render(request, "booktest/index.html", replace_data)

# 注意导包不能写 from models import BookInfo   运行会出出错的
from booktest.models import BookInfo
def show_book(request):
    bs = BookInfo.objects.all()  # 获取所有书的对象
    replace_data = dict(
        book_objs=bs
    )
    return render(request, "booktest/books.html", replace_data)


from booktest.models import HeroInfo
def hero_info(request, book_id):
    # 这是获取 HeroInfo 表中的所有英雄
    # hs = HeroInfo.objects.all()

    # get只能获取单条数据，如果是多条数据，就会报错，如果只有一条，这不会报错，html模板里的循环就会报错
    # HeroInfo.objects.get(id=book_id)


    # 获取指定id的书这个对象
    book_obj = BookInfo.objects.get(id=book_id)      # 一条数据，不用循环的话，就用get

    # 获取指定书中的英雄,为空不会报错，也不会进到模板的循环中去
    # hs = HeroInfo.objects.filter(hbook_id=book_id)  # 注意这个字段名
    # 除了filter这种写法，还有：本就获取到了 book_obj 这本书的对象，那就
    hs = book_obj.heroinfo_set.all()


    replace_data = dict(
        hero_objs=hs,
        book_obj=book_obj
    )
    return render(request, "booktest/heros.html", replace_data)   # 注意路径前往别写成了booktest.heros.html


import datetime
from django.http import HttpResponseRedirect
def create(request):
    # 创建一本书，为了简单，信息都是固定的
    b = BookInfo()  # 新建一个对象
    b.btitle = "这是新建的一本固定的书"
    b.bpub_date = datetime.date(1997, 6, 27)
    b.save()  # 把创建的数据报存

    # 上面操作完了，还是重定向(就是再次访问)回这个原来的页面（一定要的）用于展示
    return HttpResponseRedirect("/index/book")

from django.shortcuts import redirect
def delete(request, book_id):
    b = BookInfo.objects.get(id=book_id)    # 是objects，别写错了
    b.delete()    # 删除

    # return HttpResponseRedirect("/index/book")
    return redirect("/index/book")  # 跟上面效果一模一样，推荐这个吧


def login(request):
    """显示登录页面"""
    return render(request, "booktest/login.html")


def login_check(request):
    """
    request.POST
    request.GET    这俩都是<class 'django.http.request.QueryDict'>类型
    request传过来的对象的数据都在这个里面
    """
    print(type(request.POST))   # 类型是<class 'django.http.request.QueryDict'>
    print(request.method)  # 获取请求方式，一般为 POST 或 GET
    # 我们表单设计的是POST方式，浏览器直接敲这个地址 /login_check 访问的方式是GET

    # 1.获取提交的用户名和密码 (html中的input标签中的name值是什么，这里的key就是什么)
    userName = request.POST.get("userName")
    password = request.POST.get("password")
    # 2.数据库查询用户名、密码进行校验，这里就是模拟一下
    if userName == "admin" and password == "123":
        # 成功，那就跳转到一个页面
        return redirect("/index/123/")
    else:
        return HttpResponse("错误！")