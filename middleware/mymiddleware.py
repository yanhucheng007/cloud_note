from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.core import mail
import traceback
ip_address = {}
class MyMiddleware(MiddlewareMixin):

    def process_request(self,request):
        pass
        # url = request.path_info
        # if url == '/usr/reg':
        #     ip = request.META['REMOTE_ADDR']
        #     if ip in ip_address.keys():
        #         ip_address[ip] += 1
        #     else:
        #         ip_address[ip] = 1
        #     print(ip_address[ip])
        #     if ip_address[ip] > 5:
        #         return HttpResponse('time too many')
    def process_view(self,request,callback,callback_args,callback_kwargs):
        pass
    def process_response(self,request,response):
        return response
    def process_exception(self,request,exception):

        message = '发生异常：%s' % traceback
        from_email = '2769853086@qq.com'
        title = '云笔记出错！'
        recipient_list =['2158173707@qq.com']
        mail.send_mail(subject=title, message=message, from_email=from_email,
                       recipient_list=recipient_list)
        return HttpResponse('----发生错误----')
