import csv
import sys
import time
import tkinter
import traceback
from logging import error
from tkinter import *
from tkinter import messagebox as mess
from tkinter import ttk

from telethon import client
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser

window = Tk()
v = IntVar()
isChange = False
lstMember = []
lstValueCbb = []

try:
    api_id = your_api_id
    api_hash = your_api_hash
    phone = your_phone
    client = TelegramClient(phone, api_id, api_hash)
    print("Ket noi thanh cong")
except KeyError:
    print("Ket noi khong thanh cong")


def initUI():
    lstMember.clear()
    window.title("Clone pha tele 1")
    window.geometry("800x660")
    window['bg'] = "#00ccff"
    # Kiểm tra kết nối
    if not isConnecting():
        tkinter.Label(text="Nhap ma xac nhan: ")
        inputtxt = Text(window, height=1.6, width=20, bg="light yellow")
        inputtxt.pack(pady=5)

        btnConnect = tkinter.Button(
            window, text="Lay ma code", bg="#ff3300", command=lambda: checkConnectLogin())
        btnConnect.pack(pady=20)

    else:
        btnGetListGroups = tkinter.Button(
            window, text="Lay danh sach nhom", bg="#ff3300", command=lambda: getListGroups())
        btnGetListGroups.pack(pady=20)

        g2 = tkinter.Label(text="Group nhan: ")
        g2.place(x=450, y=480)

        g3 = tkinter.Label(text="Nhap so luong thanh vien toi da can add: ")
        g3.place(x=450, y=550)
        inputtxt_numMember = Text(
            window, height=1.5, width=20, bg="light yellow")
        inputtxt_numMember.place(x=450, y=570)

        btnChangeMembers = tkinter.Button(
            window, text="Chuyen members", bg="#009999", command=lambda: addMemberToGroup())
        btnChangeMembers.place(x=450, y=630)

        g0 = tkinter.Label(text="Chọn Group: ")
        g0.place(x=50, y=480)

        n = tkinter.StringVar()
        m_cbbNameGroup = ttk.Combobox(window, width=25, textvariable=n, height=100)
        if len(lstValueCbb) > 0:
            m_cbbNameGroup["values"] = lstValueCbb
        else:
            m_cbbNameGroup["values"] = 'Chua khoi tao'
        m_cbbNameGroup.place(x=130, y=480)

        m_cbbNameGroup2 = ttk.Combobox(window, width=25, height=100)
        if len(lstValueCbb) > 0:
            m_cbbNameGroup2["value"] = lstValueCbb
        else:
            m_cbbNameGroup2["value"] = 'Chua khoi tao'
        m_cbbNameGroup2.place(x=540, y=480)

        m_btnRefresh = tkinter.Button(window, text="Refresh", bg="red", command=lambda: initComboBox())
        m_btnRefresh.place(x=335, y=480)

        btnAddMembers = tkinter.Button(
            window, text="Add member vao file", bg="#009999", command=lambda: addMemberToFile())
        btnAddMembers.place(x=50, y=550)

        g0 = tkinter.Label(
            text="Chu y add members vao file truoc khi chuyen members", bg="RED")
        g0.place(x=50, y=600)

    # def test():
    #
    #     demo = InputUser(user_id=1653212137, access_hash=7165455850498097162)
    #     t = functions.contacts.DeleteContactsRequest([demo])
    #     print(t)

    # Kết nối khi chưa đăng nhập
    def checkConnectLogin():
        txt_idlogin = inputtxt.get("1.0", "end-1c")
        client.sign_in(phone, txt_idlogin)
        getStatusConnect()

    def getListGroups():
        chats = []
        groups = []
        last_date = None
        chunk_size = 200

        result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        if result is not None:
            chats.extend(result.chats)
            if chats:
                for chat in chats:
                    try:
                        if chat.megagroup:
                            groups.append(chat)
                    finally:
                        continue
                i = 0
                # Giao diện hiển thị nhóm
                game_frame = Frame(window)
                game_frame.pack(pady=10)
                # scrollbar
                game_scroll = Scrollbar(game_frame)
                game_scroll.pack(side=RIGHT, fill=Y)
                game_scroll = Scrollbar(game_frame, orient='horizontal')
                game_scroll.pack(side=BOTTOM, fill=X)
                my_game = ttk.Treeview(
                    game_frame, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)
                my_game.pack()
                game_scroll.config(command=my_game.yview)
                game_scroll.config(command=my_game.xview)
                # define our column

                my_game['columns'] = ('player_id', 'player_name', 'player_Rank')
                # format our column
                my_game.column("#0", width=0, stretch=NO)
                my_game.column("player_id", anchor=CENTER, width=100)
                my_game.column("player_name", anchor=CENTER, width=200)
                my_game.column("player_Rank", anchor=CENTER, width=150)
                # Create Headings
                my_game.heading("#0", text="", anchor=CENTER)
                my_game.heading("player_id", text="ID", anchor=CENTER)
                my_game.heading("player_name", text="TenGroup", anchor=CENTER)
                my_game.heading("player_Rank", text="SoLuongThanhVien", anchor=CENTER)

                for x in groups:
                    # print(x)
                    my_game.insert(parent='', index='end', iid=i, text='',
                                   values=(x.id, x.title, x.participants_count))
                    print("----------------")
                    print("id nhom: " + str(x.id))
                    print("Ten nhom" + str(x.title.encode('utf-8')))
                    print("----------------")
                    lstMember.append(x)
                    i = i + 1
                my_game.pack()

    def initComboBox():
        initListValue()
        time.sleep(2)
        if len(lstValueCbb) > 0:
            m_cbbNameGroup["values"] = lstValueCbb
            m_cbbNameGroup.current(0)
            m_cbbNameGroup2["value"] = lstValueCbb
            m_cbbNameGroup2.current(0)
        else:
            mess.showinfo(
                "Thong bao", "Chưa khởi tạo")

    def addMemberToFile():
        if isInitListMember():
            value = m_cbbNameGroup.get()
            if not value or value is None or value.title() == "":
                mess.showinfo(
                    "Thong bao", "Đã xảy ra lỗi vui lòng thử lại")
            else:
                print(value)
                index = getIndexList(value)
                if index == -1:
                    mess.showinfo(
                        "Thong bao", "ID nhom ko hop le, vui long thu lai")
                else:
                    chats = []
                    groups = []
                    last_date = None
                    chunk_size = 200

                    result = client(GetDialogsRequest(
                        offset_date=last_date,
                        offset_id=0,
                        offset_peer=InputPeerEmpty(),
                        limit=chunk_size,
                        hash=0
                    ))
                    chats.extend(result.chats)
                    for chat in chats:
                        try:
                            if chat.megagroup:
                                groups.append(chat)
                        finally:
                            continue

                    target_group = groups[int(index)]
                    print("Ban dang chon group: " + str(target_group.title.encode('utf-8')))

                    all_participants = client.get_participants(
                        target_group, aggressive=False)
                    print('Dang luu vao file thong tin members')
                    time.sleep(2)
                    with open("members.csv", "w", encoding='UTF-8') as f:
                        writer = csv.writer(f, delimiter=",", lineterminator="\n")
                        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id', 'SDT'])
                        for user in all_participants:
                            if user.username:
                                username = user.username
                            else:
                                username = ""
                            if user.first_name:
                                first_name = user.first_name
                            else:
                                first_name = ""
                            if user.last_name:
                                last_name = user.last_name
                            else:
                                last_name = ""
                            name = (first_name + ' ' + last_name).strip()
                            writer.writerow(
                                [username, user.id, user.access_hash, name, target_group.title, target_group.id,
                                 user.phone])
                    print('Them member vao nhom thanh coong.')
        else:
            mess.showinfo("Thong bao", "Chua lay danh sach nhom")

    def addMemberToGroup():
        valueCbb1 = m_cbbNameGroup.get()
        valueCbb2 = m_cbbNameGroup2.get()
        if valueCbb1 == valueCbb2:
            mess.showinfo("Thong bao", "Hai nhom khong duoc trung")
        else:
            index = getIndexList(valueCbb2)
            if index == -1:
                mess.showinfo("Thong bao", "ID nhom ko hop le, vui long thu lai")
            else:
                numberMember = inputtxt_numMember.get("1.0", "end-1c")
                if numberMember is None or numberMember == "":
                    mess.showinfo("Thong bao", "Chua nhap so luong thanh vien can add")
                else:
                    numberMember = int(numberMember)
                    users = []
                    with open("members.csv", encoding='UTF-8') as f:
                        rows = csv.reader(f, delimiter=",", lineterminator="\n")
                        next(rows, None)
                        for row in rows:
                            user = {}
                            user['username'] = row[0]
                            try:
                                user['id'] = int(row[1])
                                user['access_hash'] = int(row[2])
                            except IndexError:
                                print('users without id or access_hash')
                            users.append(user)

                    # random.shuffle(users)
                    chats = []
                    last_date = None
                    chunk_size = 10
                    groups = []

                    result = client(GetDialogsRequest(
                        offset_date=last_date,
                        offset_id=0,
                        offset_peer=InputPeerEmpty(),
                        limit=chunk_size,
                        hash=0
                    ))
                    chats.extend(result.chats)

                    for chat in chats:
                        try:
                            if chat.megagroup:  # CONDITION TO ONLY LIST MEGA GROUPS.
                                groups.append(chat)
                        except:
                            continue

                    target_group = groups[int(index)]
                    print("Ban dang chon group: " + target_group.title)

                    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

                    error_count = 0
                    count = 0

                    for user in users:
                        try:
                            print("Adding {}".format(user['username']))
                            if user['username'] == "":
                                user_to_add = InputPeerUser(user['id'], user['access_hash'])
                                count = count + 1
                                time.sleep(2)
                            else:
                                user_to_add = client.get_input_entity(user['username'])
                                count = count + 1
                                time.sleep(2)
                            try:
                                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                                time.sleep(2)

                            except Exception as e:
                                print("spam protection: " + e.message + ": " + str(e))

                            # print("Waiting 60 Seconds...")
                            # time.sleep(60)
                            if count == numberMember:
                                mess.showinfo("Thong bao", "Da add du " + str(numberMember) + " nguoi")
                                break

                        except PeerFloodError:
                            print(error)
                        except UserPrivacyRestrictedError:
                            print(error)
                        finally:
                            traceback.print_exc()
                            print("Unexpected Error")
                            error_count += 1
                            if error_count > 10:
                                sys.exit('too many errors')
                            continue


client.connect()


def isConnecting():
    if not client.is_user_authorized():
        # client.send_code_request(phone)
        # client.sign_in(phone, input('[+] Enter the code: '))
        return False
    else:
        return True


def getStatusConnect():
    if isConnecting():
        message_connect = "Da ket noi"
        txtMessage = tkinter.Label(text=message_connect, bg="green")
        txtMessage.place(x=700, y=10)
    else:
        message_connect = "Chua ket noi"
        txtMessage = tkinter.Label(text=message_connect, bg="red")
        txtMessage.place(x=500, y=10)


def isInitListMember():
    return len(lstMember) > 0 and len(lstValueCbb) > 0


def initListValue():
    lstValueCbb.clear()
    for x in lstMember:
        lstValueCbb.append(str(x.id) + " -- " + x.title)


def getIndexList(value):
    for i in range(len(lstValueCbb)):
        if lstValueCbb[i] == value:
            return i
    return -1


# Khởi tạo giao diện
initUI()
getStatusConnect()
window.mainloop()
