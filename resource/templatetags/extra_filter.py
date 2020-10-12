from django.template.library import Library

register=Library()

ext_list=["doc", "docx", "exe", "pdf", "ppt", "rar", "txt", "xlsx", "zip"]


@register.filter("ext")
def image_ext(value):

    return value if value in ext_list else "unknow"
@register.filter("check")
def check_sex(value):

    if value=="m":
        return "男"
    elif value=="f":
        return "女"
    else:
        return "保密"

@register.filter
def sub(value, args):
    return int(value) - int(args)