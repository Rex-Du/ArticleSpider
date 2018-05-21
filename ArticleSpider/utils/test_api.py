# AuthorName : DuQing
# CreateTime : 2017-09-26 18:14
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookie.txt')

headers1 = {
    "Host":"www.zhihu.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36"
    }
headers2 = {
    "Host":"www.zhihu.com",
    # "Referer":"https://www.zhihu.com/question/65768007",
    "authorization": "Bearer Mi4xdVRvSUJnQUFBQUFBY01JeFJ5TnVEQmNBQUFCaEFsVk4yeUQwV1FDYlF0akhIZEhUTlk4T1NiSVVNRk9KbzNTYmdR|1506579419|13eece09d3179438af41b8f8e0fef932734d9923",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36"
    }
url1 = 'https://www.zhihu.com/question/65768007'
url2 = 'https://www.zhihu.com/api/v4/questions/65768007/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default'
res = session.get(url=url1, headers=headers1)
print(session.cookies)
session.cookies.save()
res2 = session.get(url=url2, headers=headers2)
print(res2.text)

