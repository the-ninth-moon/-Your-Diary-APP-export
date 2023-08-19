import requests
import os
import tkinter as tk


# prepare for login
# get different diary
# 1 获得每天对应编号
# 2 获得日记

def write_diary2txt(id='29581504', headers=None):
    r = requests.get('https://nideriji.cn/api/diary/' + id, headers=headers)
    diary = r.json()['diary']
    time = diary['ts'].split()[0]
    weekday = diary['weekday']
    # print(time,weekday)
    with open(time + '.txt', 'w', encoding='utf-8') as f:
        f.write(time + ' ' + weekday + '\n')
        f.write(diary['title'] + '\n')
        f.write(diary['content'])


# download_diary()

def get_days_id(year=2023, month=3, headers=None):
    r = requests.get('https://nideriji.cn/api/diary/simple_by_month/' + str(year) + '/' + str(month) + '/',
                     headers=headers)
    id_dict = r.json()['diaries']
    return id_dict
    # print(id_dict)


def download_diary_by_month(year=2023, month=3, headers=None):
    pwd = os.getcwd()
    dirname = str(year) + '-' + str(month)
    try:
        os.mkdir(dirname)
    except:
        pass
    os.chdir(dirname)
    id_dict = get_days_id(year, month, headers)
    for i in id_dict:
        write_diary2txt(str(id_dict[i]), headers)
    os.chdir(pwd)


def download(ey, em, sy, sm):
    print(ey, em, sy, sm)
    headers = get_headers(e_u.get(), e_ps.get())
    while ey > sy or (ey == sy and em >= sm):
        pwd = os.getcwd()
        try:
            print("正在获取%d年%d月的日记。" % (ey, em))
            download_diary_by_month(ey, em, headers)
        except Exception as e:
            print("发生了异常：", e, "，您可以自行处理或者尝试联系作者。")
        os.chdir(pwd)
        em = em - 1
        if em == 0:
            em = 12
            ey -= 1
    print("%d-%d至%d-%d日记爬取完成。" % (sy, sm, ey, em))


def get_headers(email, ps):
    print(email, ps)
    data = {
        'csrfmiddlewaretoken': 'lKsJooKKQjQurVwSZUqDho90nH1NvONx',
        'email': email,
        'password': ps
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    # get token
    r = requests.post('https://nideriji.cn/api/login/', headers=headers, data=data)
    headers['auth'] = 'token ' + r.json()['token']
    return headers


end_year = 2023
end_month = 8

start_year = 2020
start_month = 1

root = tk.Tk()
root.title("【你的日记】导出，仅供学习交流使用，代码完全开源")

group0 = tk.LabelFrame(root, width=500, height=120)
group0.grid(row=0, column=0, sticky='n')

label_user = tk.Label(group0, text="邮箱：")
label_user.grid(row=0, column=0)

label_pw = tk.Label(group0, text="密码：")
label_pw.grid(row=1, column=0)
label_sy = tk.Label(group0, text="开始年份：")
label_sy.grid(row=2, column=0)
label_sm = tk.Label(group0, text="开始月份：")
label_sm.grid(row=3, column=0)
label_ey = tk.Label(group0, text="结束年份：")
label_ey.grid(row=4, column=0)
label_em = tk.Label(group0, text="结束月份：")
label_em.grid(row=5, column=0)

e_u = tk.Entry(group0, width=40)
e_u.grid(row=0, column=1, padx=10, pady=10)
e_ps = tk.Entry(group0, width=40)
e_ps.grid(row=1, column=1, padx=10, pady=10)
e_sy = tk.Entry(group0, width=40)
e_sy.grid(row=2, column=1, padx=10, pady=10)
e_sm = tk.Entry(group0, width=40)
e_sm.grid(row=3, column=1, padx=10, pady=10)
e_ey = tk.Entry(group0, width=40)
e_ey.grid(row=4, column=1, padx=10, pady=10)
e_em = tk.Entry(group0, width=40)
e_em.grid(row=5, column=1, padx=10, pady=10)

e_u.insert(0, "输入邮箱")
e_ps.insert(0, "输入密码")
e_sy.insert(0, "2022")
e_sm.insert(0, "12")
e_ey.insert(0, "2023")
e_em.insert(0, "7")

button0 = tk.Button(group0, text="确认",
                    command=lambda: download(int(e_ey.get()), int(e_em.get()), int(e_sy.get()), int(e_sm.get())),
                    width=10, height=3)
button0.grid(row=6, column=0, )

button1 = tk.Button(group0, text="退出", command=lambda: root.destroy(), width=10, height=3)
button1.grid(row=6, column=1)

tk.mainloop()
