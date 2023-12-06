from flask import session
import pymongo
from datetime import *
import re
import urllib.parse

host = "natek-ntp.5stm1lg.mongodb.net"
username = "nat"
password = "Abcd@1234"  

myclient = pymongo.MongoClient(f'mongodb+srv://{username}:{urllib.parse.quote_plus(password)}@{host}/')
mydb = myclient["ntp-ofc"]

def get_colection():
    return  mydb.list_collection_names()


def Insert_one(mydict,collect):
    mycol = mydb[collect]
    x = mycol.insert_one(mydict)
    print(x.inserted_id)

def Find_query(key,value,collect):
    mycol = mydb[collect]
    myquery = {key:value}
    mydoc = mycol.find(myquery, {'_id': 0}).sort('STT_PHIEUDX',pymongo.DESCENDING)
    list_mydoc=[]
    for x in mydoc:
        list_mydoc.append(x)
    return list_mydoc

def Find_myquery(myquery,collect):
    mycol = mydb[collect]
    mydoc = mycol.find(myquery, {'_id': 0}).sort('STT_PHIEUDX',pymongo.DESCENDING)
    list_mydoc=[]
    for x in mydoc:
        list_mydoc.append(x)
    return list_mydoc

def Count_myquery(myquery,collect):
    mycol = mydb[collect]
    mydoc = mycol.count_documents(myquery)
    return mydoc
   

def Find_myquery_sort(myquery,sort,collect):
    mycol = mydb[collect]
    mydoc = mycol.find(myquery, {'_id': 0}).sort(sort,pymongo.DESCENDING)
    list_mydoc=[]
    for x in mydoc:
        list_mydoc.append(x)
    return list_mydoc

def Find_myquery_sort_ASC(myquery,sort,collect):
    mycol = mydb[collect]
    mydoc = mycol.find(myquery, {'_id': 0}).sort(sort,1)
    list_mydoc=[]
    for x in mydoc:
        list_mydoc.append(x)
    return list_mydoc

def Find_all(collect):
    list_mydoc=[]
    mycol = mydb[collect]
    for x in mycol.find({}, {'_id': 0}):
        list_mydoc.append(x)
    return list_mydoc

def danh_sach_chuc_vu(collect):
    list_mydoc=[]
    mycol = mydb[collect]
    mydoc=mycol.find().sort('CHUCVU',pymongo.DESCENDING)
    for x in mydoc:
        list_mydoc.append(x)
    return list_mydoc

def danh_sach_khoa_phong(collect):
    list_mydoc=[]
    mycol = mydb[collect]
    for x in mycol.find({},{'_id': 0}).sort('TENGOIKHOAPHONG',pymongo.ASCENDING):
        list_mydoc.append(x)
    return list_mydoc

def Update_one(key1,value1,key2,value2,collect):
    mycol = mydb[collect]
    myquery = { key1: value1 }
    newvalues = { "$set": { key2:value2 } }
    mycol.update_one(myquery, newvalues)
#    for x in mycol.find():
    print('UPDATE THANH CONG')

def kiem_tra_STT_PHIEUDX_hop_le(STT_PHIEUDX):
    collect=STT_PHIEUDX
    collect=collect[:2]
    mycol = mydb[collect]
    for x in mycol.find({},{"STT_PHIEUDX":1 }):
        if x['STT_PHIEUDX']==STT_PHIEUDX:
            return True

def kiem_tra_STT_PHIEUDX_hop_le_home_lanh_dao(STT_PHIEUDX,DONVINHAN):
    resul=Find_myquery({'DONVINHAN':DONVINHAN,'STT_PHIEUDX':STT_PHIEUDX},STT_PHIEUDX[:2])
    if resul==[]:
        return False
    else:
        return True


def delete(key,value,collect):
    mycol = mydb[collect]
    myquery = { key: value }
    mycol.delete_one(myquery)

def Delete_one(key,value):
    import os
    nd=doc_thong_tin_phieu(value)
    if nd['DUONGDAN_LUUVB']!="":
        if kiem_tra_file_ton_tai(nd['DUONGDAN_LUUVB'])==True:
            os.remove(nd['DUONGDAN_LUUVB'])
    collect=value
    collect=collect[:2]
    mycol = mydb[collect]
    myquery = { key: value }
    mycol.delete_one(myquery)

def xoa_phieu(STT_PHIEUDX):
    ds=Find_query('STT_PHIEUDX',STT_PHIEUDX,STT_PHIEUDX[:2])
    for i in ds:
        Delete_one('STT_PHIEUDX',i['STT_PHIEUDX'])

def Delete_user(key,value,collect):
    Update_one(key,value,'TRANGTHAi',False,collect)

def kiem_tra_dang_nhap_hop_le(MANHANVIEN,MATKHAU):
    key='MANHANVIEN'
    value=MANHANVIEN
    collect='danh_muc_nhan_vien'
    a=Find_query(key,value,collect)
    for i in a:
        if i['MATKHAU']==MATKHAU:
            return i['HOTEN']
        else:
            return False

def kiem_tra_chuc_vu(MANHANVIEN):
    a=Find_query('MANHANVIEN',MANHANVIEN,'danh_muc_nhan_vien')
    for nhan_vien in a:
        if nhan_vien['rule_level']== '1':
            return True
        # elif  nhan_vien['MA_CV']== '004':
        #     return True
        # elif nhan_vien['MA_CV']== '005':
        #     return True
        # elif nhan_vien['MA_CV']== '006':
        #     return True
        # elif nhan_vien['MA_CV']== '010':
        #     return True
        # elif nhan_vien['MA_CV']== '011':
        #     return True
        # elif nhan_vien['MA_CV']== '01010':
        #     return True
        # elif nhan_vien['MA_CV']== '012':
        #     return True
        else: return False

def MANHANVIEN_HOTEN(MANHANVIEN):
    a=Find_query('MANHANVIEN',MANHANVIEN,'danh_muc_nhan_vien')
    for nhan_vien in a:
        return nhan_vien['HOTEN']


def HOTEN_MANHANVIEN(HOTEN):
    a=Find_query('HOTEN',HOTEN,'danh_muc_nhan_vien')
    for nhan_vien in a:
        return nhan_vien['MANHANVIEN']

def TENGOIKHOAPHONG_MAKHOAPHONG(TENGOIKHOAPHONG):
    #a=Find_query('TENGOIKHOAPHONG',TENGOIKHOAPHONG,'danh_muc_nhan_vien')
    a=Find_query('TENGOIKHOAPHONG',TENGOIKHOAPHONG,'danh_muc_khoa_phong')
    for nhan_vien in a:
        return nhan_vien['MAKHOAPHONG']

def MAKHOAPHONG_TENGOIKHOAPHONG(MAKHOAPHONG):
    #a=Find_query('MAKHOAPHONG',MAKHOAPHONG,'danh_muc_nhan_vien')
    a=Find_query('MAKHOAPHONG',MAKHOAPHONG,'danh_muc_khoa_phong')
    for nhan_vien in a:
        return nhan_vien['TENGOIKHOAPHONG']

def MA_CV_CHUCVU(MA_CV):
    a=Find_query('MACV',MA_CV,'danh_muc_chuc_vu')
    for nhan_vien in a:
        return nhan_vien['CHUCVU'], nhan_vien['rule_level']


def doc_thong_tin_nhan_vien(MANHANVIEN):
    a=Find_query('MANHANVIEN',MANHANVIEN,'danh_muc_nhan_vien')
    for info in a:
        return info



def tim_thong_tin_phieu(STT_PHIEUDX):
    collect=STT_PHIEUDX
    collect=collect[:2]
    ds=[]
    list_danh_sach=Find_query('STT_PHIEUDX',STT_PHIEUDX,collect)
    for i in list_danh_sach:
        if i['LOAIPHIEU'] !="9":
            ds.append(i)
    return ds

# def tim_thong_tin_phieu_home_lanh_dao(STT_PHIEUDX,DONVINHAN):
#     collect=STT_PHIEUDX
#     collect=collect[:2]
#     list_danh_sach=Find_query('STT_PHIEUDX',STT_PHIEUDX,collect)
#     return list_danh_sach
    

#def danh_sach_ban_giam_doc():
#    list_danh_sach=Find_query('TENGOIKHOAPHONG','Ban Giám Đốc','danh_muc_nhan_vien')
#    return list_danh_sach

def danh_sach_nhan_vien():
    mycol = mydb['danh_muc_nhan_vien']
    myquery = {'TRANGTHAi':True}
    mydoc = mycol.find(myquery, {'_id': 0}).sort('HOTEN',pymongo.ASCENDING)
    list_mydoc=[]
    for x in mydoc:
        list_mydoc.append(x)
    return list_mydoc
    
def danh_sach_nhan_vien_theo_khoa_phong(TENGOIKHOAPHONG):
    # ds=[]
    # list_danh_sach=danh_sach_nhan_vien()
    # for i in list_danh_sach:
    #     if i['TENGOIKHOAPHONG']==TENGOIKHOAPHONG:
    #         ds.append(i)
    ds=Find_myquery({'TENGOIKHOAPHONG':TENGOIKHOAPHONG,'TRANGTHAi':True},'danh_muc_nhan_vien')
    return ds


def tao_phieu_moi(MANHANVIEN,noi_dung,ly_do,LOAIPHIEU,DUONGDAN_LUUVB):
    import time
    #time.sleep(3)
    STT_PHIEUDX_=datetime.now().strftime('%y%m%d%H%M%S')
    if Find_myquery({'STT_PHIEUDX':STT_PHIEUDX_},'22')==[]:
        STT_PHIEUDX=STT_PHIEUDX_
    else:
        return False
    GIO_DEXUAT=datetime.now().strftime('%H:%M')
    NGAYNHAP=datetime.now().strftime('%d/%m/%Y')
    if LOAIPHIEU=='1':
        DIENGIAI_PHIEU='Phiếu yêu cầu'
        DUONGDAN_LUUVB=""
        DINHKEM=""
    elif LOAIPHIEU=='0':
        DIENGIAI_PHIEU='Phiếu trình'
        if DUONGDAN_LUUVB==None:
            DUONGDAN_LUUVB=""
            DINHKEM=""
        else:
            DUONGDAN_LUUVB=DUONGDAN_LUUVB
            DINHKEM="1"
    info_nhan_vien =doc_thong_tin_nhan_vien(MANHANVIEN)
    mydict={
                "id":str(datetime.now().strftime('%y%m%d%H%M%S%f'))+"_"+str(session.get('TENGOIKHOAPHONG')),
                "MASOQUANLY": str(STT_PHIEUDX)+str(LOAIPHIEU), 
                "STT_PHIEUDX":str(STT_PHIEUDX)+str(LOAIPHIEU), 
                "LOAIPHIEU": LOAIPHIEU, 
                "DIENGIAI_PHIEU": DIENGIAI_PHIEU, 
                "XULY_CVVB": "0", 
                "GIO_DEXUAT":GIO_DEXUAT, 
                "NGAYNHAP": NGAYNHAP, 
                "DONVI_DEXUAT":info_nhan_vien['MAKHOAPHONG'], 
                "DONVIDEXUAT": info_nhan_vien['TENGOIKHOAPHONG'], 
                "LOAIDEXUAT": "0", 
                "NGUOI_DEXUAT":info_nhan_vien['MANHANVIEN'],
                "HOTENNHAP": info_nhan_vien['HOTEN'], 
                "DIENGIAI_DEXUAT": noi_dung, 
                "DIENGIAI_LYDO": ly_do, 
                "DINHKEM": DINHKEM, 
                "DUONGDAN_LUUVB": DUONGDAN_LUUVB, 
                "TIEPNHAN_VT": "0", 
                "GIO_TIEPNHAN_VT": "", 
                "NGAY_TIEPNHAN_VT": "", 
                "DONVI_TIEPNHAN_VT": "", 
"DONVIVANTHU": "0136", 
"NGUOI_TIEPNHAN_VT": "", 
"HOTENVANTHU": "", 
"YKIEN_TIEPNHAN_VT": "", 
"DUYET_BGD": "0", 
"GIO_DUYET": "", 
"NGAY_DUYET": "", 
"YKIEN_BGD": "", 
"NGUOI_DUYET": "", 
"HOTENDUYET": "", 
"THOIHAN_HT": "", 
"NGAY_HT": "", 
"NHANPHIEU": "", 
"GIO_NHANPHIEU": "", 
"NGAY_NHANPHIEU": "", 
"DONVI_NHANPHIEU": "", 
"DONVINHAN": "", 
"NGUOI_NHANPHIEU": "", 
"HOTENNHANPHIEU": "", 
"TIEPNHAN": "0", 
"GIO_TIEPNHAN": "", 
"NGAY_TIEPNHAN": "", 
"DONVI_TIEPNHAN": "", 
"DONVITIEPNHAN": "", 
"NGUOI_TIEPNHAN": "", 
"HOTENTIEPNHAN": "", 
"YKIEN_TIEPNHAN": "", 
"XULY": "0", 
"DIENGIAI": "", 
"GIO_XULY": "", 
"NGAY_XULY": "", 
"DONVI_XULY": "", 
"DONVIXULY": "", 
"NGUOI_XULY": "", 
"HOTENXULY": "", 
"NOIDUNG_XULY": "", 
"HOANTAT": "", 
"NGAY_HOANTAT": "", 
"DIENMIENGIAM": "0", 
"CHUCDANH": "", 
"SOBENHAN": "", 
"CODE_BN": "", 
"HOTEN_BN": "", 
"GIOITINH": "", 
"NGAYSINH": "", 
"DIACHICUTRU_HK": "", 
"DIACHICUTRU_TT": "",
"DOIUONG_MG": "", 
"SOTHEBHYT": "", 
"DIAPHUONG": "", 
"DIAPHUONG_XN": "",
"KHOA_XN": "", 
"LOAI_XACNHAN": "",
"NHAPVIEN": "", 
"XUATVIEN": "", 
"CHANDOAN": "", 
"NOIDIEUTRI": "", 
"TENNOIDIEUTRI": "", 
"DIENBIENBENH": "", 
"HOANCANHGIADINH": "", 
"SOTIENTAMUNG": "0", 
"TONGCHIPHI": "0", 
"SOTIEN_GIAM": "0", 
"LOAI_MIENGIAM": "0", 
"TYLE_MIENGIAM": "0", 
"PHONG": "0", 
"TIEN_PHONG": "0", 
"DICHVU": "0", 
"TIEN_DICHVU": "0", 
"THUOC": "0", 
"TIEN_THUOC": "0", 
"CLS": "0", 
"TIEN_CLS": "0", 
"KHAUHAO": "0", 
"TIEN_KHAUHAO": "0", 
"KHAC": "0", 
"TIEN_KHAC": "0", 
"DIENGIAI_KHAC": "", 
"LOAI_QUY": "0", 
"TIEN_MG_DUYET": "0", 
"HUYPHIEU": "0", 
"THAYDOI": "0"
}
    collect=STT_PHIEUDX
    collect=collect[:2] # lấy 2 ký tư đầu của STT_PHIEUDX
    Insert_one(mydict,collect)
    return STT_PHIEUDX

def tao_phieu_mien_giam(MANHANVIEN,noi_dung,ly_do,TENNOIDIEUTRI,CODE_BN,NHAPVIEN,XUATVIEN,CHANDOAN,DIACHICUTRU_TT,HOTEN_BN,GIOITINH,NGAYSINH,LOAIPHIEU,SOTHEBHYT,SOBENHAN,DIAPHUONG_XN,KHOA_XN,DIENBIENBENH,HOANCANHGIADINH,SOTIENTAMUNG,TONGCHIPHI,SOTIENCONLAI):
    STT_PHIEUDX=datetime.now().strftime('%y%m%d%H%M%S')
    GIO_DEXUAT=datetime.now().strftime('%H:%M')
    NGAYNHAP=datetime.now().strftime('%d/%m/%Y')
    DIENGIAI_PHIEU='Phiếu Miễn Giảm'
    DUONGDAN_LUUVB=""
    DINHKEM=""
    info_nhan_vien =doc_thong_tin_nhan_vien(MANHANVIEN)
    if HOTEN_BN=="":
        HOTEN_BN=info_nhan_vien['HOTEN']
    if GIOITINH=="":
        GIOITINH=info_nhan_vien['GIOITINH']
    if NGAYSINH=="":
        NGAYSINH=info_nhan_vien['NGAYSINH']
    mydict={
                "id":datetime.now().strftime('%y%m%d%H%M%S%f'),
                "MASOQUANLY": STT_PHIEUDX, 
                "STT_PHIEUDX":STT_PHIEUDX, 
                "LOAIPHIEU": LOAIPHIEU, 
                "DIENGIAI_PHIEU": DIENGIAI_PHIEU, 
                "XULY_CVVB": "0", 
                "GIO_DEXUAT":GIO_DEXUAT, 
                "NGAYNHAP": NGAYNHAP, 
                "DONVI_DEXUAT":info_nhan_vien['MAKHOAPHONG'], 
                "DONVIDEXUAT": info_nhan_vien['TENGOIKHOAPHONG'], 
                "LOAIDEXUAT": "0", 
                "NGUOI_DEXUAT":info_nhan_vien['MANHANVIEN'],
                "HOTENNHAP": info_nhan_vien['HOTEN'], 
                "DIENGIAI_DEXUAT": noi_dung, 
                "DIENGIAI_LYDO": ly_do, 
                "DINHKEM": DINHKEM, 
                "DUONGDAN_LUUVB": DUONGDAN_LUUVB, 
                "TIEPNHAN_VT": "0", 
                "GIO_TIEPNHAN_VT": "", 
                "NGAY_TIEPNHAN_VT": "", 
                "DONVI_TIEPNHAN_VT": "", 
"DONVIVANTHU": "0136", 
"NGUOI_TIEPNHAN_VT": "", 
"HOTENVANTHU": "", 
"YKIEN_TIEPNHAN_VT": "", 
"DUYET_BGD": "0", 
"GIO_DUYET": "", 
"NGAY_DUYET": "", 
"YKIEN_BGD": "", 
"NGUOI_DUYET": "", 
"HOTENDUYET": "", 
"THOIHAN_HT": "", 
"NGAY_HT": "", 
"NHANPHIEU": "", 
"GIO_NHANPHIEU": "", 
"NGAY_NHANPHIEU": "", 
"DONVI_NHANPHIEU": "", 
"DONVINHAN": "", 
"NGUOI_NHANPHIEU": "", 
"HOTENNHANPHIEU": "", 
"TIEPNHAN": "0", 
"GIO_TIEPNHAN": "", 
"NGAY_TIEPNHAN": "", 
"DONVI_TIEPNHAN": "", 
"DONVITIEPNHAN": "", 
"NGUOI_TIEPNHAN": "", 
"HOTENTIEPNHAN": "", 
"YKIEN_TIEPNHAN": "", 
"XULY": "0", 
"DIENGIAI": "", 
"GIO_XULY": "", 
"NGAY_XULY": "", 
"DONVI_XULY": "", 
"DONVIXULY": "", 
"NGUOI_XULY": "", 
"HOTENXULY": "", 
"NOIDUNG_XULY": "", 
"HOANTAT": "0", 
"NGAY_HOANTAT": "", 
"DIENMIENGIAM": "0", 
"CHUCDANH": info_nhan_vien['CHUCVU'], 
"SOBENHAN": SOBENHAN, 
"CODE_BN": CODE_BN, 
"HOTEN_BN": HOTEN_BN,
"GIOITINH": GIOITINH,
"NGAYSINH": NGAYSINH,
"DIACHICUTRU_HK": "", 
"DIACHICUTRU_TT": DIACHICUTRU_TT,
"DOIUONG_MG": "", 
"SOTHEBHYT": SOTHEBHYT, 
"DIAPHUONG": "", 
"DIAPHUONG_XN": DIAPHUONG_XN,
"KHOA_XN": KHOA_XN, 
"LOAI_XACNHAN": "",
"NHAPVIEN": NHAPVIEN, 
"XUATVIEN": XUATVIEN, 
"CHANDOAN": CHANDOAN, 
"NOIDIEUTRI": "", 
"TENNOIDIEUTRI": TENNOIDIEUTRI, 
"DIENBIENBENH": DIENBIENBENH, 
"HOANCANHGIADINH": HOANCANHGIADINH, 
"SOTIENTAMUNG": SOTIENTAMUNG, 
"TONGCHIPHI": TONGCHIPHI, 
"SOTIEN_GIAM": SOTIENCONLAI, 
"LOAI_MIENGIAM": "0", 
"TYLE_MIENGIAM": "0", 
"PHONG": "0", 
"TIEN_PHONG": "0", 
"DICHVU": "0", 
"TIEN_DICHVU": "0", 
"THUOC": "0", 
"TIEN_THUOC": "0", 
"CLS": "0", 
"TIEN_CLS": "0", 
"KHAUHAO": "0", 
"TIEN_KHAUHAO": "0", 
"KHAC": "0", 
"TIEN_KHAC": "0", 
"DIENGIAI_KHAC": "", 
"LOAI_QUY": "0", 
"TIEN_MG_DUYET": "0", 
"HUYPHIEU": "0", 
"THAYDOI": "0"
}
    collect=STT_PHIEUDX
    collect=collect[:2] # lấy 2 ký tư đầu của STT_PHIEUDX
    Insert_one(mydict,collect)
    return STT_PHIEUDX

def tao_phieu_cong_van_van_ban_moi(MANHANVIEN,noi_dung,ly_do,DUONGDAN_LUUVB,DONVINHAN,so_phieu_van_ban_den,so_van_ban_den,thoi_han_hoan_thanh):
    info_nhan_vien =doc_thong_tin_nhan_vien(MANHANVIEN)
    mydict={
                "id":datetime.now().strftime('%y%m%d%H%M%S%f'),
                "MASOQUANLY": datetime.now().strftime('%y%m%d%H%M%S')+'9', 
                "STT_PHIEUDX":datetime.now().strftime('%y%m%d%H%M%S')+'9', 
                "LOAIPHIEU": '9', 
                "DIENGIAI_PHIEU": 'Công văn - Văn bản', 
                'so_phieu_van_ban_den':so_phieu_van_ban_den,
                'so_van_ban_den':so_van_ban_den,
                "XULY_CVVB": "0", 
                "GIO_DEXUAT":datetime.now().strftime('%H:%M'), 
                "NGAYNHAP": datetime.now().strftime('%Y/%m/%d'), 
                "DONVI_DEXUAT":"009", 
                "DONVIDEXUAT": "Ban Giám Đốc", 
                "LOAIDEXUAT": "0", 
                "NGUOI_DEXUAT":info_nhan_vien['MANHANVIEN'],
                "HOTENNHAP": info_nhan_vien['HOTEN'], 
                "DIENGIAI_DEXUAT": noi_dung, 
                "DIENGIAI_LYDO": ly_do, 
                "DINHKEM": '1', 
                "DUONGDAN_LUUVB": DUONGDAN_LUUVB, 
                "TIEPNHAN_VT": "1", 
                "GIO_TIEPNHAN_VT": datetime.now().strftime('%H:%M'), 
                "NGAY_TIEPNHAN_VT": datetime.now().strftime('%Y/%m/%d'), 
                "DONVI_TIEPNHAN_VT": "", 
"DONVIVANTHU": "0130", 
"NGUOI_TIEPNHAN_VT": info_nhan_vien['MANHANVIEN'], 
"HOTENVANTHU": info_nhan_vien['HOTEN'], 
"YKIEN_TIEPNHAN_VT": "", 
"DUYET_BGD": "1", 
"GIO_DUYET": datetime.now().strftime('%H:%M'), 
"NGAY_DUYET": datetime.now().strftime('%Y/%m/%d'), 
"YKIEN_BGD": DONVINHAN, 
"NGUOI_DUYET": "CHV67059501", 
"HOTENDUYET": "Võ Đức Chiến", 
"THOIHAN_HT": thoi_han_hoan_thanh, 
"NGAY_HT": "", 
"NHANPHIEU": "", 
"GIO_NHANPHIEU": "", 
"NGAY_NHANPHIEU": "", 
"DONVI_NHANPHIEU": "", 
"DONVINHAN": DONVINHAN, 
"NGUOI_NHANPHIEU": "", 
"HOTENNHANPHIEU": "", 
"TIEPNHAN": "0", 
"GIO_TIEPNHAN": "", 
"NGAY_TIEPNHAN": "", 
"DONVI_TIEPNHAN": "", 
"DONVITIEPNHAN": DONVINHAN, 
"NGUOI_TIEPNHAN": "", 
"HOTENTIEPNHAN": "", 
"YKIEN_TIEPNHAN": "", 
"XULY": "", 
"DIENGIAI": "", 
"GIO_XULY": "", 
"NGAY_XULY": "", 
"DONVI_XULY": "", 
"DONVIXULY": "", 
"NGUOI_XULY": "", 
"HOTENXULY": "", 
"NOIDUNG_XULY": "", 
"HOANTAT": "0", 
"NGAY_HOANTAT": "", 
"DIENMIENGIAM": "0", 
"CHUCDANH": "", 
"SOBENHAN": "", 
"CODE_BN": "", 
"HOTEN_BN": "", 
"GIOITINH": "", 
"NGAYSINH": "", 
"DIACHICUTRU_HK": "", 
"DIACHICUTRU_TT": "",
"DOIUONG_MG": "", 
"SOTHEBHYT": "", 
"DIAPHUONG": "", 
"DIAPHUONG_XN": "",
"KHOA_XN": "", 
"LOAI_XACNHAN": "",
"NHAPVIEN": "", 
"XUATVIEN": "", 
"CHANDOAN": "", 
"NOIDIEUTRI": "", 
"TENNOIDIEUTRI": "", 
"DIENBIENBENH": "", 
"HOANCANHGIADINH": "", 
"SOTIENTAMUNG": "0", 
"TONGCHIPHI": "0", 
"SOTIEN_GIAM": "0", 
"LOAI_MIENGIAM": "0", 
"TYLE_MIENGIAM": "0", 
"PHONG": "0", 
"TIEN_PHONG": "0", 
"DICHVU": "0", 
"TIEN_DICHVU": "0", 
"THUOC": "0", 
"TIEN_THUOC": "0", 
"CLS": "0", 
"TIEN_CLS": "0", 
"KHAUHAO": "0", 
"TIEN_KHAUHAO": "0", 
"KHAC": "0", 
"TIEN_KHAC": "0", 
"DIENGIAI_KHAC": "", 
"LOAI_QUY": "0", 
"TIEN_MG_DUYET": "0", 
"HUYPHIEU": "0", 
"THAYDOI": "0"
}
    collect=mydict['STT_PHIEUDX']
    collect=collect[:2] # lấy 2 ký tư đầu của STT_PHIEUDX
    Insert_one(mydict,collect)
    return mydict['STT_PHIEUDX']

def danh_sach_phieu_chua_duyet(MANHANVIEN,STT_PHIEUDX,LOAIPHIEU):
    ds=[]
    collect=STT_PHIEUDX
    # print(collect)
    collect=collect[:2]
    list_mydoc=Find_query('NGUOI_DEXUAT',MANHANVIEN,collect)
    for i in list_mydoc:
        if i['TIEPNHAN_VT']=="0" and i['LOAIPHIEU']==LOAIPHIEU:
            ds.append(i)
    return ds

def van_thu_tiep_nhan_phieu(STT_PHIEUDX,HOTEN):
    GIO_TIEPNHAN_VT=datetime.now().strftime('%H:%M')
    NGAY_TIEPNHAN_VT=datetime.now().strftime('%d/%m/%Y')
    DONVI_TIEPNHAN_VT='0136'
    DONVIVANTHU='Bộ Phận Tiếp Nhận'
    NGUOI_TIEPNHAN_VT=HOTEN_MANHANVIEN(HOTEN)
    HOTENVANTHU=HOTEN
    TIEPNHAN_VT='1'
    collect=STT_PHIEUDX
    collect=collect[:2]
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'TIEPNHAN_VT',TIEPNHAN_VT,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENVANTHU',HOTENVANTHU,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_TIEPNHAN_VT',NGUOI_TIEPNHAN_VT,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVIVANTHU',DONVIVANTHU,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVI_TIEPNHAN_VT',DONVI_TIEPNHAN_VT,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_TIEPNHAN_VT',NGAY_TIEPNHAN_VT,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_TIEPNHAN_VT',GIO_TIEPNHAN_VT,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'TIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENTIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_TIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVITIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVI_TIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_TIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_TIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVI_XULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVIXULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'YKIEN_TIEPNHAN',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENXULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_XULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOANTAT',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_XULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_XULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NOIDUNG_XULY',"",collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_HOANTAT',"",collect)

def bgd_duyet_phieu(STT_PHIEUDX,YKIEN_BGD,HOTENDUYET,DONVINHAN):
    GIO_DUYET=datetime.now().strftime('%H:%M')
    NGAY_DUYET=datetime.now().strftime('%d/%m/%Y')
    DUYET_BGD='1'
    collect=STT_PHIEUDX
    collect=collect[:2]
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_DUYET',GIO_DUYET,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_DUYET',NGAY_DUYET,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DUYET_BGD',DUYET_BGD,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'YKIEN_BGD',YKIEN_BGD,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENDUYET',HOTENDUYET,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVINHAN',DONVINHAN,collect)

def nhan_vien_nhanphieu(STT_PHIEUDX,HOTENNHANPHIEU):
    GIO_NHANPHIEU=datetime.now().strftime('%H:%M')
    NGAY_NHANPHIEU=datetime.now().strftime('%d/%m/%Y')
    NHANPHIEU='1'
    collect=STT_PHIEUDX
    collect=collect[:2]
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_NHANPHIEU',GIO_NHANPHIEU,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_NHANPHIEU',NGAY_NHANPHIEU,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'NHANPHIEU',NHANPHIEU,collect)
    Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENNHANPHIEU',HOTENNHANPHIEU,collect)
    


def lanh_dao_tiep_nhan_phieu(id,STT_PHIEUDX,DONVI_TIEPNHAN,DONVITIEPNHAN,NGUOI_TIEPNHAN,HOTENTIEPNHAN):
    GIO_TIEPNHAN=datetime.now().strftime('%H:%M')
    NGAY_TIEPNHAN=datetime.now().strftime('%d/%m/%Y')
    TIEPNHAN='1'
    collect=STT_PHIEUDX
    collect=collect[:2]
    Update_one('id',id,'TIEPNHAN',TIEPNHAN,collect)
    Update_one('id',id,'HOTENTIEPNHAN',HOTENTIEPNHAN,collect)
    Update_one('id',id,'NGUOI_TIEPNHAN',NGUOI_TIEPNHAN,collect)
    Update_one('id',id,'DONVITIEPNHAN',DONVITIEPNHAN,collect)
    Update_one('id',id,'DONVI_TIEPNHAN',DONVI_TIEPNHAN,collect)
    Update_one('id',id,'NGAY_TIEPNHAN',NGAY_TIEPNHAN,collect)
    Update_one('id',id,'GIO_TIEPNHAN',GIO_TIEPNHAN,collect)
    Update_one('id',id,'DONVI_XULY',DONVI_TIEPNHAN,collect)
    Update_one('id',id,'DONVIXULY',DONVITIEPNHAN,collect)
    Update_one('id',id,'YKIEN_TIEPNHAN',"",collect)
    Update_one('id',id,'HOTENXULY',"",collect)
    Update_one('id',id,'NGUOI_XULY',"",collect)
    Update_one('id',id,'HOANTAT',"",collect)
    Update_one('id',id,'GIO_XULY',"",collect)
    Update_one('id',id,'NGAY_XULY',"",collect)
    Update_one('id',id,'NOIDUNG_XULY',"",collect)
    Update_one('id',id,'NGAY_HOANTAT',"",collect)

    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'TIEPNHAN',TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENTIEPNHAN',HOTENTIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_TIEPNHAN',NGUOI_TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVITIEPNHAN',DONVITIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVI_TIEPNHAN',DONVI_TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_TIEPNHAN',NGAY_TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_TIEPNHAN',GIO_TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVI_XULY',DONVI_TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'DONVIXULY',DONVITIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'YKIEN_TIEPNHAN',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENXULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOANTAT',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NOIDUNG_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_HOANTAT',"",collect)

def lanh_dao_chuyen_phieu(id,STT_PHIEUDX,YKIEN_TIEPNHAN,HOTENXULY,NGUOI_XULY):
    collect=STT_PHIEUDX
    collect=collect[:2]
    HOANTAT='Đang Đợi Xử Lý'
    Update_one('id',id,'YKIEN_TIEPNHAN',YKIEN_TIEPNHAN,collect)
    Update_one('id',id,'HOTENXULY',HOTENXULY,collect)
    Update_one('id',id,'NGUOI_XULY',NGUOI_XULY,collect)
    Update_one('id',id,'HOANTAT',HOANTAT,collect)
    Update_one('id',id,'GIO_XULY',"",collect)
    Update_one('id',id,'NGAY_XULY',"",collect)
    Update_one('id',id,'NOIDUNG_XULY',"",collect)
    Update_one('id',id,'NGAY_HOANTAT',"",collect)


    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'YKIEN_TIEPNHAN',YKIEN_TIEPNHAN,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENXULY',HOTENXULY,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_XULY',NGUOI_XULY,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOANTAT',HOANTAT,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NOIDUNG_XULY',"",collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_HOANTAT',"",collect)

def lanh_dao_hoan_tat_xu_ly(id,STT_PHIEUDX,NOIDUNG_XULY,HOTENXULY,NGUOI_XULY):
    collect=STT_PHIEUDX
    collect=collect[:2]
    NGAY_HOANTAT=datetime.now().strftime('%d/%m/%Y')
    HOANTAT='Hoàn Tất Xử Lý'
    GIO_XULY=datetime.now().strftime('%H:%M')
    NGAY_XULY=datetime.now().strftime('%d/%m/%Y')
    Update_one('id',id,'HOTENXULY',HOTENXULY,collect)
    Update_one('id',id,'NGUOI_XULY',NGUOI_XULY,collect)
    Update_one('id',id,'NOIDUNG_XULY',NOIDUNG_XULY,collect)
    Update_one('id',id,'HOANTAT',HOANTAT,collect)
    Update_one('id',id,'NGAY_HOANTAT',NGAY_HOANTAT,collect)
    Update_one('id',id,'GIO_XULY',GIO_XULY,collect)
    Update_one('id',id,'NGAY_XULY',NGAY_XULY,collect)

    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOTENXULY',HOTENXULY,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGUOI_XULY',NGUOI_XULY,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NOIDUNG_XULY',NOIDUNG_XULY,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'HOANTAT',HOANTAT,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_HOANTAT',NGAY_HOANTAT,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'GIO_XULY',GIO_XULY,collect)
    # Update_one('STT_PHIEUDX',STT_PHIEUDX,'NGAY_XULY',NGAY_XULY,collect)


def nhan_vien_tiep_nhan_xu_ly(id,STT_PHIEUDX):
    GIO_XULY=datetime.now().strftime('%H:%M')
    NGAY_XULY=datetime.now().strftime('%d/%m/%Y')
    collect=STT_PHIEUDX
    collect=collect[:2]
    HOANTAT='Đang Xử Lý'
    Update_one('id',id,'GIO_XULY',GIO_XULY,collect)
    Update_one('id',id,'NGAY_XULY',NGAY_XULY,collect)
    Update_one('id',id,'HOANTAT',HOANTAT,collect)
    Update_one('id',id,'NOIDUNG_XULY',"",collect)
    Update_one('id',id,'NGAY_HOANTAT',"",collect)

def nhan_vien_hoan_tat_xu_ly(id,STT_PHIEUDX,NOIDUNG_XULY):
    collect=STT_PHIEUDX
    collect=collect[:2]
    if NOIDUNG_XULY=='huy':
        
        NGAY_HOANTAT=""
        HOANTAT="Đang Xử Lý"
        Update_one('id',id,'HOANTAT',HOANTAT,collect)
        Update_one('id',id,'NGAY_HOANTAT',NGAY_HOANTAT,collect)
    elif NOIDUNG_XULY=='huytiepnhan':
       
        GIO_XULY=""
        NGAY_XULY=""
        HOANTAT='Đang Đợi Xử Lý'
        Update_one('id',id,'GIO_XULY',GIO_XULY,collect)
        Update_one('id',id,'NGAY_XULY',NGAY_XULY,collect)
        Update_one('id',id,'HOANTAT',HOANTAT,collect)
    else:
        
        NGAY_HOANTAT=datetime.now().strftime('%d/%m/%Y')
        HOANTAT='Hoàn Tất Xử Lý'
        Update_one('id',id,'NOIDUNG_XULY',NOIDUNG_XULY,collect)
        Update_one('id',id,'HOANTAT',HOANTAT,collect)
        Update_one('id',id,'NGAY_HOANTAT',NGAY_HOANTAT,collect)
    


def danh_sach_phieu_dang_doi_xu_ly(HOTENXULY,STT_PHIEUDX):
    ds=[]
    collect=STT_PHIEUDX
    collect=collect[:2]
    list_mydoc=Find_query('HOTENXULY',HOTENXULY,collect)
    for i in list_mydoc:
        if i['HOANTAT']=="Đang Đợi Xử Lý"and i['DONVIXULY']==session.get('TENGOIKHOAPHONG'):
            ds.append(i)
    return ds

def danh_sach_phieu_dang_xu_ly(HOTENXULY,STT_PHIEUDX):
    ds=[]
    collect=STT_PHIEUDX
    collect=collect[:2]
    list_mydoc=Find_query('HOTENXULY',HOTENXULY,collect)
    for i in list_mydoc:
        if i['HOANTAT']=="Đang Xử Lý"and i['DONVIXULY']==session.get('TENGOIKHOAPHONG'):
            ds.append(i)
    return ds

def danh_sach_phieu_da_hoan_tat_xu_ly(HOTENXULY,STT_PHIEUDX):
    ds=[]
    collect=STT_PHIEUDX
    collect=collect[:2]
    list_mydoc=Find_query('HOTENXULY',HOTENXULY,collect)
    for i in list_mydoc:
        if i['HOANTAT']=="Hoàn Tất Xử Lý"and i['DONVIXULY']==session.get('TENGOIKHOAPHONG'):
            ds.append(i)
    return ds

def danh_sach_phieu_da_hoan_tat_xu_ly_lanh_dao(DONVIXULY,STT_PHIEUDX):
    trang_thai_xu_ly=session.get('trang_thai_xu_ly')
    collect=STT_PHIEUDX
    collect=collect[:2]
    if trang_thai_xu_ly==None:
        list_mydoc=Find_query('DONVIXULY',DONVIXULY,collect)
    else: 
        list_mydoc=Find_myquery_sort({'DONVIXULY':DONVIXULY,'HOANTAT':trang_thai_xu_ly},'NGAY_TIEPNHAN',collect)
    #list_mydoc=Find_query('DONVIXULY',DONVIXULY,collect)
    # for i in list_mydoc:
    #     if i['HOANTAT']=="Hoàn Tất Xử Lý":
    #         ds.append(i)
    return list_mydoc

def list_nam_tim_kiem():
    # set = {"2017","2018","2019","2020","2021"}
    # x= datetime.now().strftime('%Y')
    # set.add(x)
    # list_set=list(set)
    # list_set.sort(reverse = True)
    lst_colec=[]
    for i in get_colection():
        if len(i)==2:
            i="20"+i
            lst_colec.append(i)
    lst_colec.sort(reverse = True)
    return lst_colec

def danh_sach_tim_kiem_nhanh_theo_ten_nhan_vien(year,HOTENNHAP):
    collect=str(year[2:])
    ds=Find_query('HOTENNHAP',HOTENNHAP,collect)
    return ds

def danh_sach_cac_phieu_don_vi_da_tiep_nhan(year,DONVITIEPNHAN):
    collect=str(year[2:])
    # ds=Find_query('DONVITIEPNHAN',DONVITIEPNHAN,collect)
    ds=Find_myquery({'DONVITIEPNHAN':DONVITIEPNHAN,'TIEPNHAN':'1'},collect)
    return ds


def create_barcode(STT_PHIEUDX):
    xoa_barcode() # xoa barcode truoc khi tao moi
    import barcode
    from barcode.writer import ImageWriter
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(u''''''+str(STT_PHIEUDX)+'''''', writer=ImageWriter())
    duongdan='static/barcode/'+STT_PHIEUDX
    option={
        'module_width':0.2,
        'module_height':5.0,
        'quiet_zone':0.5,
        'font_size':15,
        'text_distance':1
        }
    ean.save(duongdan,option)

def xoa_barcode():
    import os
    for i in os.listdir('static/barcode/'):
        os.remove('static/barcode/'+i)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'xlsx'}
    #ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
    if '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
           return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    else:
        return False

def tinh_so_ngay_nghi(ngay_bat_dau,ngay_ket_thuc):
    from datetime import datetime
    date_format = "%d/%m/%Y"
    d0 = datetime.strptime(ngay_bat_dau, date_format)
    d1 = datetime.strptime(ngay_ket_thuc, date_format)
    delta = abs(d0 - d1)
    return delta.days

def dinh_dang_ngay(date):
    date=str(date).split('-')
    date=date[2]+'/'+date[1]+'/'+date[0]
    return date


def tao_phieu_nghi_phep(MANHANVIEN,LOAI_NGHI_PHEP,NGAY_BAT_DAU,NGAY_KET_THUC,DIA_CHI_LIEN_LAC,SO_DIEN_THOAI_LIEN_LAC,GHI_CHU,NUA_NGAY,BUOI_BAT_DAU,BUOI_KET_THUC,SO_NGAY_NGHI,NGAY_NGHI,DOI_TUONG):
    thong_tin_nhan_vien=doc_thong_tin_nhan_vien(MANHANVIEN)
    MASO_PHIEU=datetime.now().strftime('%y%m%d%H%M%S%f')
    NGAY_BAT_DAU=dinh_dang_ngay(NGAY_BAT_DAU)
    NGAY_KET_THUC=dinh_dang_ngay(NGAY_KET_THUC)
    cdnn=[i['CDNN'] for i in Find_myquery({'MANHANVIEN':MANHANVIEN},'danh_muc_nhan_vien')]
    # SO_NGAY_NGHI=tinh_so_ngay_nghi(NGAY_BAT_DAU,NGAY_KET_THUC)
    # SO_NGAY_NGHI=int(SO_NGAY_NGHI)+1
    SO_NGAY_NGHI=float(SO_NGAY_NGHI)-float(NUA_NGAY)
    SO_NGAY_NGHI=abs(SO_NGAY_NGHI)
    # if SO_NGAY_NGHI==0.5:
    #     SO_NGAY_NGHI="0.5"
    # else:
    #     SO_NGAY_NGHI=float(int(SO_NGAY_NGHI1+0.5))
    LOAI_NGHI_PHEP=str(LOAI_NGHI_PHEP).split("_")
    dict_phieu_nghi_phep={
    "id":datetime.now().strftime('%y%m%d%H%M%S%f'),
    'STT_PHIEUDX':datetime.now().strftime('%y%m%d%H%M%S'),
    'MASO_PHIEU':MASO_PHIEU,
    'MANHANVIEN':thong_tin_nhan_vien['MANHANVIEN'],
    'HOTEN':thong_tin_nhan_vien['HOTEN'],
    'TENGOIKHOAPHONG':thong_tin_nhan_vien['TENGOIKHOAPHONG'],
    'GIOITINH':thong_tin_nhan_vien['GIOITINH'],
    'NGAYSINH':thong_tin_nhan_vien['NGAYSINH'],
    'LOAI_NGHI_PHEP':LOAI_NGHI_PHEP[0],
    'NGAY_BAT_DAU':NGAY_BAT_DAU,
    'NGAY_KET_THUC':NGAY_KET_THUC,
    'SO_NGAY_NGHI':str(SO_NGAY_NGHI),
    'DIA_CHI_LIEN_LAC':DIA_CHI_LIEN_LAC,
    'SO_DIEN_THOAI_LIEN_LAC':SO_DIEN_THOAI_LIEN_LAC,
    'HO_TEN_LANH_DAO':"",
    'LANH_DAO_XAC_NHAN':'Chưa Duyệt',
    'NGAY_XAC_NHAN':"",
    'NAM':datetime.now().strftime('%Y'),
    'THANG':datetime.now().strftime('%m'),
    'NGAY':datetime.now().strftime('%d'),
    'NGAY_TAO_PHIEU':datetime.now().strftime('%d/%m/%Y'),
    'GIO_TAO_PHIEU':datetime.now().strftime('%H:%M:%S'),
    'GHI_CHU':GHI_CHU,
    'BUOI_BAT_DAU':BUOI_BAT_DAU,
    'BUOI_KET_THUC':BUOI_KET_THUC,
    'NGAY_NGHI':NGAY_NGHI,
    'DOI_TUONG':DOI_TUONG,
    "khoa_phieu":"0",
    'CDNN':cdnn[0],
    'ky_hieu':LOAI_NGHI_PHEP[1]
    }
    query={
        'MANHANVIEN':thong_tin_nhan_vien['MANHANVIEN'],
        'NGAY_BAT_DAU':NGAY_BAT_DAU,
        'NGAY_KET_THUC':NGAY_KET_THUC,
        'BUOI_BAT_DAU':BUOI_BAT_DAU,
        'BUOI_KET_THUC':BUOI_KET_THUC,
    }
    kq=Find_myquery(query,"nghi_phep")
    if kq == []:
        Insert_one(dict_phieu_nghi_phep,'nghi_phep')
    return MASO_PHIEU



def xoa_phieu_nghi_phep(MASO_PHIEU):
    mycol = mydb["nghi_phep"]
    myquery = { "MASO_PHIEU":MASO_PHIEU}
    mycol.delete_one(myquery) 

def danh_sach_nhan_vien_nghi_phep(MANHANVIEN):
    year=datetime.now().strftime('%Y')
    ds=[]
    list_danh_sach=Find_query('MANHANVIEN',MANHANVIEN,'nghi_phep')
    # for i in list_danh_sach:
        #if i['NAM']==year:
            # ds.append(i)
    return list_danh_sach

# def danh_sach_nhan_vien_nghi_phep_chua_duyet():
#     year=datetime.now().strftime('%Y')
#     ds=[]
#     list_danh_sach=Find_query('LANH_DAO_XAC_NHAN','Chưa Duyệt','nghi_phep')
#     for i in list_danh_sach:
#         if i['NAM']==year:
#             ds.append(i)
#     return ds

# def danh_sach_nhan_vien_nghi_phep_da_duyet():
#     year=datetime.now().strftime('%Y')
#     ds=[]
#     list_danh_sach=Find_query('LANH_DAO_XAC_NHAN','Đồng Ý Cho Nghỉ','nghi_phep')
#     for i in list_danh_sach:
#         if i['NAM']==year:
#             ds.append(i)
#     return ds
def danh_sach_nhan_vien_nghi_phep_chua_duyet(TENGOIKHOAPHONG):
    year=datetime.now().strftime('%Y')
    ds=[]
    # list_danh_sach=Find_query('LANH_DAO_XAC_NHAN','Chưa Duyệt','nghi_phep')
    myquery={
        'LANH_DAO_XAC_NHAN':'Chưa Duyệt',
        'TENGOIKHOAPHONG':TENGOIKHOAPHONG
    }
    list_danh_sach=Find_myquery(myquery,'nghi_phep')
    for i in list_danh_sach:
        # if i['NAM']==year:
            ds.append(i)
    return ds

def danh_sach_nhan_vien_nghi_phep_da_duyet(TENGOIKHOAPHONG):
    year=datetime.now().strftime('%Y')
    ds=[]
    myquery={
        # 'LANH_DAO_XAC_NHAN':'Đồng Ý Cho Nghỉ',
        'TENGOIKHOAPHONG':TENGOIKHOAPHONG
    }
    list_danh_sach=Find_myquery(myquery,'nghi_phep')
    for i in list_danh_sach:
        # if i['NAM']==year:
        if i['LANH_DAO_XAC_NHAN']=="Đồng Ý Cho Nghỉ":
            ds.append(i)
        elif i['LANH_DAO_XAC_NHAN']=="Không Đồng Ý Cho Nghỉ":
            ds.append(i)
    sort_ds=sorted(ds, key=lambda i: i['khoa_phieu'],reverse=False)
    return sort_ds

def logging(MANHANVIEN,TENGOIKHOAPHONG,HOTEN,IP,NOIDUNG):
    NGAY_GIO=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    NGAY=datetime.now().strftime('%d/%m/%Y')
    dict_log={
        'STT_PHIEUDX':datetime.now().strftime('%y%m%d%H%M%S'),
        'MANHANVIEN':MANHANVIEN,
        'TENGOIKHOAPHONG':TENGOIKHOAPHONG,
        'HOTEN':HOTEN,
        'IP':IP,
        'NGAY':NGAY,
        'NGAY_GIO':NGAY_GIO,
        'NOIDUNG':NOIDUNG
    }
    # print(dict_log)
    Insert_one(dict_log,'logging')

def hash_mk(matkhau): # hàm băm 
    import hashlib
    mk=str(hashlib.sha256(matkhau.strip().encode('utf-8')).hexdigest())
    return mk


def danh_sach_cong_van_van_ban_khoa_phong_nhan(DONVINHAN):
    danh_sach=[]
    for i in get_colection():
        if len(i)==2:
            print(i)
            #ds=Find_myquery({'LOAIPHIEU':'9','DONVINHAN':DONVINHAN,'TIEPNHAN':'0'},i)
            ds=Find_myquery({'LOAIPHIEU':'9','DONVINHAN':DONVINHAN,'so_van_ban_den':{"$not": {"$regex": "NTP"}}},i)
            for i in ds:
                danh_sach.append(i)
    # a=Find_query('LOAIPHIEU','9',datetime.now().strftime('%y'))
    # for i in a:
    #     if i['DONVINHAN']==DONVINHAN and len(i['STT_PHIEUDX'])==12:
    #         danh_sach.append(i)
    # danh_sach=Find_myquery({'LOAIPHIEU':'9','DONVINHAN':DONVINHAN,'TIEPNHAN':'0'},datetime.now().strftime('%y'))
    # danh_sach=Find_myquery({'LOAIPHIEU':'9','DONVINHAN':DONVINHAN,'TIEPNHAN':'0'},datetime.now().strftime('%y'))
    sort_ds=sorted(danh_sach, key=lambda i: i['STT_PHIEUDX'],reverse=True)
    return sort_ds

def dem_danh_sach_cong_van_van_ban_khoa_phong_nhan(DONVINHAN):
    count = 0
    for i in get_colection():
        if len(i)==2:
            print(i)
            total=Count_myquery({'LOAIPHIEU':'9','DONVINHAN':DONVINHAN,'so_van_ban_den':{"$not": {"$regex": "NTP"}}},i)
            count = count + total
              
    return count

def dem_danh_sach_cong_van_van_ban_khoa_phong_nhan_theo_trang_thai(DONVINHAN, TRANGTHAI):
    count = 0
    query = {'LOAIPHIEU':'9', 'HOANTAT': TRANGTHAI,'DONVINHAN':DONVINHAN,'so_van_ban_den':{"$not": {"$regex": "NTP"}}}

    if TRANGTHAI == 'Chưa Xử Lý':
        values_to_exclude = ['Hoàn Tất Xử Lý', 'Đang Đợi Xử Lý']
        query['HOANTAT'] = {'$nin': values_to_exclude}

    for i in get_colection():
        if len(i)==2:
            total=Count_myquery(query ,i)
            count = count + total

    return count

  

def danh_sach_cong_van_phan_trang(DONVINHAN, HOTENXULY, TRANGTHAI, SOVB, START, END, PAGESIZE, SKIPCOUNT):
    danh_sach=[]
    query = {'LOAIPHIEU':'9','so_van_ban_den':{"$not": {"$regex": "NTP"}}}
    
    if DONVINHAN is not None:
        query['DONVINHAN'] = DONVINHAN

    if START is not None and END is not None:
        start_date = datetime.strptime(START, '%Y/%m/%d')
        end_date = datetime.strptime(END, '%Y/%m/%d')
        start_date_str = start_date.strftime('%Y/%m/%d')
        end_date_str = end_date.strftime('%Y/%m/%d')
        query['NGAYNHAP'] = {'$gte': start_date_str, '$lte': end_date_str}

    if TRANGTHAI is not None:
        query['HOANTAT'] =  {'$in': TRANGTHAI}
        if 'Chưa Xử Lý' in TRANGTHAI:
            if 'Hoàn Tất Xử Lý' in TRANGTHAI:
                TRANGTHAI.remove('Hoàn Tất Xử Lý')
            if 'Đang Đợi Xử Lý' in TRANGTHAI:
                TRANGTHAI.remove('Đang Đợi Xử Lý')

            if(len(TRANGTHAI) == 1):
                TRANGTHAI.append('Hoàn Tất Xử Lý')
                TRANGTHAI.append('Đang Đợi Xử Lý')
                
            TRANGTHAI.remove('Chưa Xử Lý')
            query['HOANTAT'] =  {'$nin': TRANGTHAI}

    if HOTENXULY is not None:
        query['HOTENXULY'] = HOTENXULY

    if SOVB is not None:
        regex_pattern = re.compile(f'.*{SOVB}.*', re.IGNORECASE)
        query['$and'] = [
            {'so_van_ban_den': {'$regex': regex_pattern}},
            {'so_van_ban_den': {"$not": {"$regex": "NTP"}}}
        ]

    for i in get_colection():
        if len(i)==2:
            mycol = mydb[i]
            mydoc = mycol.find(query, {'_id': 0}).skip(SKIPCOUNT).limit(PAGESIZE).sort('STT_PHIEUDX',pymongo.DESCENDING)
            if len(danh_sach) < PAGESIZE:
                for doc in mydoc:
                    danh_sach.append(doc)
            else:
                return danh_sach
            
    return danh_sach


def dem_tong_danh_sach_cong_van_phan_trang(DONVINHAN, HOTENXULY, TRANGTHAI, SOVB, START, END):
    count = 0
    query = {'LOAIPHIEU':'9','so_van_ban_den':{"$not": {"$regex": "NTP"}}}
    
    if DONVINHAN is not None:
        query['DONVINHAN'] = DONVINHAN

    if START is not None and END is not None:
        start_date = datetime.strptime(START, '%Y/%m/%d')
        end_date = datetime.strptime(END, '%Y/%m/%d')
        start_date_str = start_date.strftime('%Y/%m/%d')
        end_date_str = end_date.strftime('%Y/%m/%d')
        query['NGAYNHAP'] = {'$gte': start_date_str, '$lte': end_date_str}

    if TRANGTHAI is not None:
        query['HOANTAT'] =  {'$in': TRANGTHAI}
        if 'Chưa Xử Lý' in TRANGTHAI:
            if 'Hoàn Tất Xử Lý' in TRANGTHAI:
                TRANGTHAI.remove('Hoàn Tất Xử Lý')
            if 'Đang Đợi Xử Lý' in TRANGTHAI:
                TRANGTHAI.remove('Đang Đợi Xử Lý')

            if(len(TRANGTHAI) == 1):
                TRANGTHAI.append('Hoàn Tất Xử Lý')
                TRANGTHAI.append('Đang Đợi Xử Lý')
                
            TRANGTHAI.remove('Chưa Xử Lý')
            query['HOANTAT'] =  {'$nin': TRANGTHAI}

    if HOTENXULY is not None:
        query['HOTENXULY'] = HOTENXULY

    if SOVB is not None:
        regex_pattern = re.compile(f'.*{SOVB}.*', re.IGNORECASE)
        query['$and'] = [
            {'so_van_ban_den': {'$regex': regex_pattern}},
            {'so_van_ban_den': {"$not": {"$regex": "NTP"}}}
        ]

    for i in get_colection():
        if len(i)==2:
            mycol = mydb[i]
            mydoc = mycol.count_documents(query)
            count = count + mydoc
            
    return count

def danh_sach_cong_van_van_ban_khoa_phong_nhan_theo_trang_thai(DONVINHAN, TRANGTHAI):
    danh_sach=[]
    query = {'LOAIPHIEU':'9', 'HOANTAT': TRANGTHAI,'DONVINHAN':DONVINHAN,'so_van_ban_den':{"$not": {"$regex": "NTP"}}}

    if TRANGTHAI == 'Chưa Xử Lý':
        values_to_exclude = ['Hoàn Tất Xử Lý', 'Đang Đợi Xử Lý']
        query['HOANTAT'] = {'$nin': values_to_exclude}

    for i in get_colection():
        if len(i)==2:
            ds=Find_myquery(query ,i)
            for i in ds:
                danh_sach.append(i)
    sort_ds=sorted(danh_sach, key=lambda i: i['STT_PHIEUDX'],reverse=True)
    return sort_ds

def danh_sach_cong_van_van_ban_khoa_phong_nhan_chua_xu_ly(DONVINHAN, take):
    values_to_exclude = ['Hoàn Tất Xử Lý', 'Đang Đợi Xử Lý']
    danh_sach=[]
    for i in get_colection():
        if len(i)==2:
            ds=Find_myquery({'LOAIPHIEU':'9','HOANTAT': {'$nin': values_to_exclude},'DONVINHAN':DONVINHAN,'so_van_ban_den':{"$not": {"$regex": "NTP"}}},i)
            for i in ds:
                if len(danh_sach) < take:
                    danh_sach.append(i)
                else:
                    sort_ds=sorted(danh_sach, key=lambda i: i['STT_PHIEUDX'],reverse=True)
                    return sort_ds
    return danh_sach
    

def danh_sach_phieu_theo_trang_thai(TENGOIKHOAPHONG,HOTENXULY,STT_PHIEUDX,TRANGTHAI):
    collect=STT_PHIEUDX
    collect=collect[:2]
    myquery = {'HOTENXULY':HOTENXULY, 'HOANTAT': TRANGTHAI, 'DONVIXULY': TENGOIKHOAPHONG}

    if TRANGTHAI is None:
        myquery = {'HOTENXULY':HOTENXULY,'DONVIXULY': TENGOIKHOAPHONG}
    
    list_mydoc= Find_myquery(myquery, collect)
    return list_mydoc

def dem_danh_sach_phieu_theo_trang_thai(TENGOIKHOAPHONG,HOTENXULY,STT_PHIEUDX,TRANGTHAI):
    collect=STT_PHIEUDX
    collect=collect[:2]
    myquery = {'HOTENXULY':HOTENXULY,'DONVIXULY': TENGOIKHOAPHONG}

    if TRANGTHAI is not None:
        myquery = {'HOTENXULY':HOTENXULY, 'HOANTAT': TRANGTHAI, 'DONVIXULY': TENGOIKHOAPHONG}
        if TRANGTHAI == 'Chưa Xử Lý':
            values_to_exclude = ['Hoàn Tất Xử Lý', 'Đang Đợi Xử Lý']
            myquery['HOANTAT'] = {'$nin': values_to_exclude}
    
    count= Count_myquery(myquery, collect)
    return count

def danh_sach_phieu_chua_xu_ly(TENGOIKHOAPHONG, HOTENXULY, STT_PHIEUDX):
    values_to_exclude = ['Hoàn Tất Xử Lý', 'Đang Đợi Xử Lý']
    collect=STT_PHIEUDX
    collect=collect[:2]
    myquery = { 'HOANTAT': {'$nin': values_to_exclude}, 'DONVIXULY': TENGOIKHOAPHONG}
    
    list_mydoc= Find_myquery(myquery, collect)
    return list_mydoc

def list_don_vi_nhan_cong_van(lst):
    ds=[]
    for i in lst:
        if i!="":
            ds.append(i)
    return ds

def kiem_tra_file_ton_tai(duongdan):
    from os import path
    kq=path.isfile(duongdan)
    return kq


def import_excel(csvFilePath,excelFilePath):
    import pandas as pd
    import csv
    lst=[]
    read_file = pd.read_excel(excelFilePath)
    read_file.to_csv(csvFilePath, index = None,header=True)
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            #dict_bn={
            #    'HOTEN':rows['Họ tên'],
            #    'NGAYSINH':rows['Ngày sinh'],
                #'GIOITINH':rows['Giới tính\n'],
            #    'DIACHI':rows['Địa chỉ']
            #}
            lst.append(rows)
    return lst

def session_nghi_phep(MASO_PHIEU):
    from flask import session
    ds=Find_query('MASO_PHIEU',MASO_PHIEU,'nghi_phep')
    for i in ds:
            session['MASO_PHIEU_NGHIPHEP']=i['MASO_PHIEU']
            session['HOTEN_NGHIPHEP']=i['HOTEN']
            session['TENGOIKHOAPHONG_NGHIPHEP']=i['TENGOIKHOAPHONG']
            session['GIOI_TINH_NGHIPHEP']=i['GIOITINH']
            session['NGAY_SINH_NGHIPHEP']=i['NGAYSINH']
            session['LOAI_NGHI_PHEP_NGHIPHEP']=i['LOAI_NGHI_PHEP']
            session['SO_NGAY_NGHI_NGHIPHEP']=str(i['SO_NGAY_NGHI'])
            session['NGAY_BAT_DAU_NGHIPHEP']=i['NGAY_BAT_DAU']
            session['NGAY_KET_THUC_NGHIPHEP']=i['NGAY_KET_THUC']
            session['DIA_CHI_LIEN_LAC_NGHIPHEP']=i['DIA_CHI_LIEN_LAC']
            session['SO_DIEN_THOAI_LIEN_LAC_NGHIPHEP']=i['SO_DIEN_THOAI_LIEN_LAC']
            session['HO_TEN_LANH_DAO_NGHIPHEP']=i['HO_TEN_LANH_DAO']
            session['LANH_DAO_XAC_NHAN_NGHIPHEP']=i['LANH_DAO_XAC_NHAN']
            session['NGAY_XAC_NHAN_NGHIPHEP']=i['NGAY_XAC_NHAN']
            session['NGAY_TAO_PHIEU_NGHIPHEP']=i['NGAY_TAO_PHIEU']
            session['NGAY_NGHIPHEP']=i['NGAY']
            session['THANG_NGHIPHEP']=i['THANG']
            session['NAM_NGHIPHEP']=i['NAM']
            session['BUOI_BAT_DAU']=i['BUOI_BAT_DAU']
            session['BUOI_KET_THUC']=i['BUOI_KET_THUC']
           

def doc_thong_tin_phieu(STT_PHIEUDX):
    collect=STT_PHIEUDX
    collect=collect[:2]
    a=Find_query('STT_PHIEUDX',STT_PHIEUDX,collect)
    for info in a:
        return info

def session_report_phieu_yeu_cau(STT_PHIEUDX):
    from flask import session, Markup
    i=doc_thong_tin_phieu(STT_PHIEUDX)
    a=str(i['NGAYNHAP']).split('/')
    ngaynhap='Tp HCM, ngày '+a[0]+' tháng '+a[1]+' năm '+a[2]
    session['STT_PHIEUDX_PYC']=i['STT_PHIEUDX']
    session['DIENGIAI_PHIEU_PYC']=i['DIENGIAI_PHIEU']
    session['NGAYNHAP_PYC']=ngaynhap
    session['DONVIDEXUAT_PYC']=i['DONVIDEXUAT']
    session['HOTENNHAP_PYC']=i['HOTENNHAP']
    session['DIENGIAI_DEXUAT_PYC']=Markup(i['DIENGIAI_DEXUAT'])
    session['DIENGIAI_LYDO_PYC']=Markup(i['DIENGIAI_LYDO'])
    session['HOTENDUYET_PYC']=i['HOTENDUYET']
    session['NGAY_DUYET_PYC']=i['NGAY_DUYET']
    session['DONVITIEPNHAN_PYC']=i['DONVITIEPNHAN']
    session['NGAY_TIEPNHAN_PYC']=i['NGAY_TIEPNHAN']
    session['HOTENXULY_PYC']=i['HOTENXULY']
    session['HOANTAT_PYC']=i['HOANTAT']
    session['NGAY_HOANTAT_PYC']=i['NGAY_HOANTAT']
    session['DONVINHAN_PYC']=i['DONVINHAN']
    session['NGAY_NHANPHIEU_PYC']=i['NGAY_NHANPHIEU']

def session_report_phieu_trinh(STT_PHIEUDX):
    from flask import session, Markup
    i=doc_thong_tin_phieu(STT_PHIEUDX)
    a=str(i['NGAYNHAP']).split('/')
    ngaynhap='Tp HCM, ngày '+a[0]+' tháng '+a[1]+' năm '+a[2]
    session['STT_PHIEUDX_PT']=i['STT_PHIEUDX']
    session['DIENGIAI_PHIEU_PT']=i['DIENGIAI_PHIEU']
    session['NGAYNHAP_PT']=ngaynhap
    session['DONVIDEXUAT_PT']=i['DONVIDEXUAT']
    session['HOTENNHAP_PT']=i['HOTENNHAP']
    session['DIENGIAI_DEXUAT_PT']=Markup(i['DIENGIAI_DEXUAT'])
    session['DIENGIAI_LYDO_PT']=Markup(i['DIENGIAI_LYDO'])
    session['HOTENDUYET_PT']=i['HOTENDUYET']
    session['NGAY_DUYET_PT']=i['NGAY_DUYET']
    session['DONVITIEPNHAN_PT']=i['DONVITIEPNHAN']
    session['HOTENTIEPNHAN_PT']=i['HOTENTIEPNHAN']
    session['YKIEN_TIEPNHAN_PT']=i['YKIEN_TIEPNHAN']
    session['NGAY_TIEPNHAN_PT']=i['NGAY_TIEPNHAN']
    session['HOTENXULY_PT']=i['HOTENXULY']
    session['HOANTAT_PT']=i['HOANTAT']
    session['NGAY_HOANTAT_PT']=i['NGAY_HOANTAT']
    session['NOIDUNG_XULY_PT']=i['NOIDUNG_XULY']

def session_report_phieu_mien_giam_nv(STT_PHIEUDX):
    from flask import session, Markup
    i=doc_thong_tin_phieu(STT_PHIEUDX)
    a=str(i['NGAYNHAP']).split('/')
    ngaynhap='Tp HCM, ngày '+a[0]+' tháng '+a[1]+' năm '+a[2]
    session['STT_PHIEUDX_MG']=i['STT_PHIEUDX']
    #session['DIENGIAI_PHIEU_PT']=i['DIENGIAI_PHIEU']
    session['NGAYNHAP_MG']=ngaynhap
    session['DONVIDEXUAT_MG']=i['DONVIDEXUAT']
    session['HOTENNHAP_MG']=i['HOTENNHAP']
    #session['DIENGIAI_DEXUAT_PT']=Markup(i['DIENGIAI_DEXUAT'])
    #session['DIENGIAI_LYDO_PT']=Markup(i['DIENGIAI_LYDO'])
    session['HOTENDUYET_MG']=i['HOTENDUYET']
    session['NGAY_DUYET_MG']=i['NGAY_DUYET']
    #session['DONVITIEPNHAN_PT']=i['DONVITIEPNHAN']
    #session['HOTENTIEPNHAN_PT']=i['HOTENTIEPNHAN']
    #session['YKIEN_TIEPNHAN_PT']=i['YKIEN_TIEPNHAN']
    #session['NGAY_TIEPNHAN_PT']=i['NGAY_TIEPNHAN']
    #session['HOTENXULY_PT']=i['HOTENXULY']
    #session['HOANTAT_PT']=i['HOANTAT']
    #session['NGAY_HOANTAT_PT']=i['NGAY_HOANTAT']
    #session['NOIDUNG_XULY_PT']=i['NOIDUNG_XULY']
    session['CHUCDANH_MG']=i['CHUCDANH']
    session['CODE_BN_MG']=i['CODE_BN']
    #session['HOTEN_BN_MG']=i['HOTEN_BN']
    session['NGAYSINH_MG']=i['NGAYSINH']
    session['DIACHICUTRU_TT_MG']=i['DIACHICUTRU_TT']
    session['NHAPVIEN_MG']=i['NHAPVIEN']
    session['XUATVIEN_MG']=i['XUATVIEN']
    session['CHANDOAN_MG']=i['CHANDOAN']
    session['TENNOIDIEUTRI_MG']=i['TENNOIDIEUTRI']

def session_report_phieu_mien_giam_than_nhan(STT_PHIEUDX):
    from flask import session, Markup
    i=doc_thong_tin_phieu(STT_PHIEUDX)
    a=str(i['NGAYNHAP']).split('/')
    ngaynhap='Tp HCM, ngày '+a[0]+' tháng '+a[1]+' năm '+a[2]
    session['STT_PHIEUDX_MGTN']=i['STT_PHIEUDX']
    #session['DIENGIAI_PHIEU_PT']=i['DIENGIAI_PHIEU']
    session['NGAYNHAP_MGTN']=ngaynhap
    session['DONVIDEXUAT_MGTN']=i['DONVIDEXUAT']
    session['HOTENNHAP_MGTN']=i['HOTENNHAP']
    #session['DIENGIAI_DEXUAT_PT']=Markup(i['DIENGIAI_DEXUAT'])
    #session['DIENGIAI_LYDO_PT']=Markup(i['DIENGIAI_LYDO'])
    session['HOTENDUYET_MGTN']=i['HOTENDUYET']
    session['NGAY_DUYET_MGTN']=i['NGAY_DUYET']
    #session['DONVITIEPNHAN_PT']=i['DONVITIEPNHAN']
    #session['HOTENTIEPNHAN_PT']=i['HOTENTIEPNHAN']
    #session['YKIEN_TIEPNHAN_PT']=i['YKIEN_TIEPNHAN']
    #session['NGAY_TIEPNHAN_PT']=i['NGAY_TIEPNHAN']
    #session['HOTENXULY_PT']=i['HOTENXULY']
    #session['HOANTAT_PT']=i['HOANTAT']
    #session['NGAY_HOANTAT_PT']=i['NGAY_HOANTAT']
    #session['NOIDUNG_XULY_PT']=i['NOIDUNG_XULY']
    session['CHUCDANH_MGTN']=i['CHUCDANH']
    session['CODE_BN_MGTN']=i['CODE_BN']
    session['HOTEN_BN_MGTN']=i['HOTEN_BN']
    session['NGAYSINH_MGTN']=i['NGAYSINH']
    session['DIACHICUTRU_TT_MGTN']=i['DIACHICUTRU_TT']
    session['NHAPVIEN_MGTN']=i['NHAPVIEN']
    session['XUATVIEN_MGTN']=i['XUATVIEN']
    session['CHANDOAN_MGTN']=i['CHANDOAN']
    session['TENNOIDIEUTRI_MGTN']=i['TENNOIDIEUTRI']

def quater_of_invoice(date):
    import math
    str_date=str(date).split('-')
    try:
        result=math.ceil(int(str_date[1])/3)
    except IndexError:
        result=""
    return str(result)

def ham_tao_phieu_giai_quyet_van_ban_den(so_van_ban_den,co_quan_ban_hanh,ngay_ban_hanh,ngay_nhan_van_ban,trich_yeu,loai_cv,stt_cv):
    if loai_cv=="CV Đến":
        temp=str(ngay_nhan_van_ban).split('-')
        ngay=temp[0]
        thang=temp[1]
        nam=temp[2]
        quy=quater_of_invoice(ngay_nhan_van_ban)
    else:
        temp=str(ngay_ban_hanh).split('-')
        ngay=temp[0]
        thang=temp[1]
        nam=temp[2]
        quy=quater_of_invoice(ngay_ban_hanh)
    dict_gqvbd={
        'so_van_ban_den':so_van_ban_den,
        'so_van_ban_hoi_dap':"",
        'co_quan_ban_hanh':co_quan_ban_hanh,
        'ngay_ban_hanh':ngay_ban_hanh,
        'ngay_nhan_van_ban':ngay_nhan_van_ban,
        'trich_yeu':trich_yeu,
        'ma_so_phieu':datetime.now().strftime('0%y%m%d%H%M%S'),
        'ngay':ngay,
        'thang':thang,
        'nam':nam,
        'quy':quy,
        'loai_cv':loai_cv,
        'stt_cv':stt_cv,
        'dinh_kem':""
    }
    Insert_one(dict_gqvbd,'phieu_giai_quyet_van_ban_den')
   

def ham_xoa_phieu_giai_quyet_van_ban(ma_so_phieu):
    mycol = mydb["phieu_giai_quyet_van_ban_den"]
    myquery = { "ma_so_phieu": ma_so_phieu }
    mycol.delete_one(myquery)

def format_date(date):
    date=str(date).split('-')
    date=date[2]+"-"+date[1]+"-"+date[0]
    return date

# def busday(ngay_bat_dau,ngay_ket_thuc):
#     import pandas as pd
#     days=[]
#     holi_day=[]
#     res=pd.bdate_range(start=ngay_bat_dau,end=ngay_ket_thuc)
#     for i in res:
#         i=str(i).replace(' 00:00:00','')
#         days.append(i)
#     print(len(days))
#     res=set(days)-set(holi_day)
#     return len(res),list(res)

def find_holiday(collect,db):
    mydb = myclient[db]
    list_mydoc=[]
    mycol = mydb[collect]
    for x in mycol.find({}, {'_id': 0}):
        list_mydoc.append(x)
    return list_mydoc

def busday(ngay_bat_dau,ngay_ket_thuc,weekmask,holiday):
    import pandas as pd
    days=[]
    # holi_day=[i['ngay_holiday'] for i in Find_all('holiday','QL_TCCB')]
    # print(holi_day)
    # weekmask = 'Sun Mon Tue Wed Thu Fri Sat'
    res=pd.bdate_range(start=ngay_bat_dau,end=ngay_ket_thuc,weekmask=weekmask,freq='C')
    for i in res:
        i=str(i).replace(' 00:00:00','')
        days.append(i)
    #print(len(days))
    res=set(days)-set(holiday)
    return len(res),list(res)


def rule_level(macv):
    level=[i['rule_level'] for i in Find_myquery({"MACV":macv},'danh_muc_chuc_vu')]
    return level[0]

def cap_nhat_ngay_nghi_phep(MANHANVIEN):
    import numpy as np
    query={
        'MANHANVIEN':MANHANVIEN
    }
    data=Find_myquery(query,'chi_tiet_nghi_phep')
    so_ngay_nghi=[j['SO_NGAY_NGHI'] for j in data]
    tong=np.sum(so_ngay_nghi)
    Update_one('MANHANVIEN',MANHANVIEN,'so_ngay_nghi_phep_trong_nam',int(tong),'danh_muc_nhan_vien')

def thong_ke_ngay_nghi_thuong_nien(ngay_bat_dau,ngay_ket_thuc,TENGOIKHOAPHONG):
    import pandas as pd
    import numpy as np
    myquery={
        'khoa_phieu':'1',
        "TENGOIKHOAPHONG":TENGOIKHOAPHONG,
        'NGAY_NGHI':{"$gte":ngay_bat_dau , "$lte":ngay_ket_thuc }
    }
    data=Find_myquery(myquery,'chi_tiet_nghi_phep')
    if data==[]:
        myquery={
        'khoa_phieu':'1',
        "TENGOIKHOAPHONG":TENGOIKHOAPHONG,
        'NGAY_NGHI':{"$gte":ngay_ket_thuc , "$lte":ngay_bat_dau }
    }
        data=Find_myquery(myquery,'chi_tiet_nghi_phep')
    df=pd.DataFrame(data)
    try:
        df['SO_NGAY_NGHI']=pd.to_numeric(df['SO_NGAY_NGHI'])
    except KeyError:
        return '''<div class="alert alert-danger"><strong>No Data</strong></div>'''
    df=df.pivot_table(index=['LOAI_NGHI_PHEP','HOTEN'],columns=['NGAY_NGHI'],values='SO_NGAY_NGHI',aggfunc=np.sum)
    df.fillna('')
    df=df.to_clipboard()
    df=pd.read_clipboard()
    df.insert(2,'Tổng','0')
    df['Tổng']=df.sum(axis=1,numeric_only=True)
    df=df.fillna('')
    html=df.to_html(classes='table table-striped',table_id="THONGKE",justify='left')
    html=html.replace('NGAY_TRONG_TUAN','')
    html=html.replace('NGAY_NGHI','')
    html=html.replace('Unnamed: 1','')
    print(df)
    return html

def thoi_gian_cong_tac(ngay_tuyen_dung):
    import pandas as pd
    from datetime import datetime
    weekmask = 'Sun Mon Tue Wed Thu Fri Sat'
    ngay_tuyen_dung=str(ngay_tuyen_dung).split('/')
    try:
        y=ngay_tuyen_dung[2]
        m=ngay_tuyen_dung[1]
        d=ngay_tuyen_dung[0]
    except IndexError:
        so_nam_cong_tac=0
        phep_tang_them=0
        return int(so_nam_cong_tac) ,int(phep_tang_them)
    ngay_bat_dau=y+'-'+m+'-'+d
    ngay_ket_thuc=datetime.now().strftime('%Y-%m-%d')
    res=pd.bdate_range(start=ngay_bat_dau,end=ngay_ket_thuc,weekmask=weekmask,freq='C')
    so_nam_cong_tac=len(res)/365
    phep_tang_them=len(res)/1825
    return int(so_nam_cong_tac) ,int(phep_tang_them)

def lich_su_xem_van_ban(so_phieu_van_ban_den,hoten,khoa_phong):
    myquery={
        "so_phieu_van_ban_den":so_phieu_van_ban_den,
        'ho_ten':hoten,
        'khoa_phong':khoa_phong,
        'ngay_gio_xem':datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    kq=Find_myquery({"so_phieu_van_ban_den":so_phieu_van_ban_den,'ho_ten':hoten,'khoa_phong':khoa_phong},'lich_su_xem_van_ban')
    if kq==[]:
        Insert_one(mydict=myquery,collect='lich_su_xem_van_ban')
    else:
        Update_one('_id',str(so_phieu_van_ban_den+hoten+khoa_phong),'ngay_gio_xem',datetime.now().strftime('%d/%m/%Y %H:%M:%S'),'lich_su_xem_van_ban')

def ket_qua_xu_ly_van_ban(so_phieu_van_ban_den):
    colects=get_colection()
    lis=[]
    for colect in colects:
        kq=Find_myquery({'so_phieu_van_ban_den':so_phieu_van_ban_den,"LOAIPHIEU":"9","HOANTAT":"Hoàn Tất Xử Lý"},colect)
        if kq !=[]:
            for i in kq:
                string=str(i['DONVIXULY'])+" "+str(i['NGAY_HOANTAT'])
                lis.append(string)
    return lis