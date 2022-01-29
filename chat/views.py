# from django.http import HttpResponseRedirect, JsonResponse
# from django.views import View
# from graphql_auth.models import UserStatus
#
# class ActivateView(View):
#     def get(self, request, **kwargs):
#        try:
#           token = str(kwargs.get("token"))
#           print("zzzzzzzzzzzzzzzzzzz:" + token)
#           UserStatus.verify(token=token)
#        except Exception as e:
#           print(e)
#           # return HttpResponseRedirect("/some/error/url")
#        # return HttpResponseRedirect("/activate/thankyou")
#        return JsonResponse({"aaa": "bbb"})