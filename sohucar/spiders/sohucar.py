from scrapy import Selector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import urllib.parse as urlparse
import json
import regex

class sohucar(CrawlSpider):
    name = "sohucar"
    start_urls = ['http://db.auto.sohu.com/home']

    def parse(self, response):
        sel = Selector(response)
        brandlist = sel.xpath('//li[@class="close_child"]') 
        for brand in brandlist :
            brandname = brand.xpath('./h4[@class="brand_tit"]/a/text()').extract()
            #brandname = regex.sub('<[^>]+>', '', brandname)
            brandname = brandname[1]
            carSerieslist = brand.xpath('./ul[@class="tree_con"]')
            for carSeries in carSerieslist :
                carSeriesname = carSeries.xpath('./li[@class="con_tit"]/a/text()').extract()
                #carSeriesname = regex.sub('<[^>]+>', '', carSeriesname)
                carSeriesname = carSeriesname[1].strip()
                carlist = carSeries.xpath('./li/a[@class="model-a"]')
                for car in carlist :
                    carname = car.xpath('./text()').extract()
                    carid = car.xpath('./@id').extract_first()
                    carname = carname[1]
                    carid = carid.replace('m' ,'')
                    #url = 'http://db.auto.sohu.com/api/para/data/model_%s.json' % (carid)
                    url = 'http://db.auto.sohu.com/api/model/select/trims_%s.json?callback=jQuery183005710185070441576_1515933574075&_=1515933574535' % (carid)
                    yield Request(url=url ,callback=self.parse_carlist, meta={'brandname': brandname, 'carSeriesname': carSeriesname, 'carname': carname})

#    def parse_carlist(self, response):
#        metadict = response.meta
#        carinfor = json.loads(response.body_as_unicode())
#        carlist = carinfor.get('SIP_M_TRIMS')
#        for car in carlist:
#            url = 'http://db.auto.sohu.com/api/para/data/trim_%s.json' % (car.get('SIP_T_ID'))
#            yield Request(url=url ,meta={'name': car.get('SIP_T_NAME'), 'year': car.get('SIP_T_YEAR'),
#            'disp': car.get('SIP_T_DISP'), 'loc': car.get('SIP_T_LOC'), 'sta': car.get('SIP_T_STA'),
#            'gear': car.get('SIP_T_GEAR'), 'meta': metadict} ,callback=self.parse_cardata)
    
    def parse_carlist(self, response):
        metadict = response.meta
        carinforlist = regex.search(r'(\{.*\})', response.body_as_unicode())
        carinforlist = json.loads(carinforlist.group(1))
        carinforlist = carinforlist.get('trimyears')        
        for carinfor in carinforlist:
            for carinfo in carinfor.get('trims'):
                url = 'http://db.auto.sohu.com/api/para/data/trim_%s.json' % (carinfo.get('tid'))
                yield Request(url=url ,meta={'name': carinfo.get('tname'), 'year': carinfor.get('y'),
            'status': carinfo.get('status'), 'price': carinfo.get('price'), 'brandname': metadict.get('brandname')
            , 'carSeriesname': metadict.get('carSeriesname')} ,callback=self.parse_cardata)



    def parse_cardata(self, response):
        metadict = response.meta
        carinfo=[]
        carinfo.append(metadict.get('name'))
        carinfo.append(metadict.get('year'))
        carinfo.append(metadict.get('status'))
        carinfo.append(metadict.get('price'))
        carinfo.append(metadict.get('brandname'))
        carinfo.append(metadict.get('carSeriesname'))
        infordictlist = [
 #{'id': 'SIP_C_102', 'name': '\r\n\t\t\t\t\t\t\t'},
 {'id': 'SIP_C_103', 'name': '4S店最低报价'},
 {'id': 'SIP_C_104', 'name': '车厂'},
 {'id': 'SIP_C_105', 'name': '级别'},
 {'id': 'SIP_C_106', 'name': '车体结构'},
 {'id': 'SIP_C_293', 'name': '长x宽x高(mm)'},
 {'id': 'SIP_C_107', 'name': '发动机'},
 {'id': 'SIP_C_108', 'name': '变速箱'},
 {'id': 'SIP_C_303', 'name': '动力类型：'},
 {'id': 'SIP_C_112', 'name': '官方最高车速(km/h)'},
 {'id': 'SIP_C_294', 'name': '工信部油耗(L/100km)'},
 {'id': 'SIP_C_113', 'name': '官方0-100加速(s)'},
 {'id': 'SIP_C_114', 'name': '保养周期'},
 {'id': 'SIP_C_304', 'name': '保养费用：'},
 {'id': 'SIP_C_115', 'name': '保修政策'},
 {'id': 'SIP_C_116', 'name': '碰撞星级'},
 {'id': 'SIP_C_295', 'name': '更多实测参数：'},
 {'id': 'SIP_C_117', 'name': '长度(mm)'},
 {'id': 'SIP_C_118', 'name': '宽度(mm)'},
 {'id': 'SIP_C_119', 'name': '高度(mm)'},
 {'id': 'SIP_C_120', 'name': '轴距(mm)'},
 {'id': 'SIP_C_121', 'name': '前轮距(mm)'},
 {'id': 'SIP_C_122', 'name': '后轮距(mm)'},
 {'id': 'SIP_C_123', 'name': '整备质量(kg)'},
 {'id': 'SIP_C_124', 'name': '车身结构'},
 {'id': 'SIP_C_125', 'name': '车门数(个)'},
 {'id': 'SIP_C_126', 'name': '座位数(个)'},
 {'id': 'SIP_C_127', 'name': '油箱容积(L)'},
 {'id': 'SIP_C_128', 'name': '行李厢容积(L)'},
 {'id': 'SIP_C_129', 'name': '最小离地间隙(mm)'},
 {'id': 'SIP_C_130', 'name': '最小转弯半径(m)'},
 {'id': 'SIP_C_131', 'name': '接近角(°)'},
 {'id': 'SIP_C_132', 'name': '离去角(°)'},
 {'id': 'SIP_C_134', 'name': '发动机描述'},
 {'id': 'SIP_C_135', 'name': '发动机型号'},
 {'id': 'SIP_C_136', 'name': '排量(L)'},
 {'id': 'SIP_C_137', 'name': '汽缸容积(cc)'},
 {'id': 'SIP_C_138', 'name': '工作方式'},
 {'id': 'SIP_C_139', 'name': '汽缸数(个)'},
 {'id': 'SIP_C_140', 'name': '汽缸排列形式'},
 {'id': 'SIP_C_141', 'name': '每缸气门数(个)'},
 {'id': 'SIP_C_142', 'name': '气门结构'},
 {'id': 'SIP_C_143', 'name': '压缩比'},
 {'id': 'SIP_C_297', 'name': '最大马力(ps)'},
 {'id': 'SIP_C_298', 'name': '最大功率(kW/rpm)'},
 {'id': 'SIP_C_299', 'name': '最大扭矩(N·m/rpm)'},
 {'id': 'SIP_C_148', 'name': '升功率(kW/l)'},
 {'id': 'SIP_C_305', 'name': '混合类型：'},
 {'id': 'SIP_C_306', 'name': '插电形式：'},
 {'id': 'SIP_C_307', 'name': '电动机最大功率(kW)：'},
 {'id': 'SIP_C_308', 'name': '电动机最大扭矩：'},
 {'id': 'SIP_C_309', 'name': '最大行驶里程(km)：'},
 {'id': 'SIP_C_310', 'name': '电池种类：'},
 {'id': 'SIP_C_311', 'name': '电池容量(kWh)：'},
 {'id': 'SIP_C_149', 'name': '燃料'},
 {'id': 'SIP_C_150', 'name': '供油方式'},
 {'id': 'SIP_C_151', 'name': '缸盖材料'},
 {'id': 'SIP_C_152', 'name': '缸体材料'},
 {'id': 'SIP_C_155', 'name': '排放标准'},
 {'id': 'SIP_C_156', 'name': '变速箱简称'},
 {'id': 'SIP_C_157', 'name': '挡位个数'},
 {'id': 'SIP_C_158', 'name': '变速箱类型'},
 {'id': 'SIP_C_307', 'name': '电动机最大功率(kW)：'},
 {'id': 'SIP_C_308', 'name': '电动机最大扭矩：'},
 {'id': 'SIP_C_309', 'name': '最大行驶里程(km)：'},
 {'id': 'SIP_C_310', 'name': '电池种类：'},
 {'id': 'SIP_C_311', 'name': '电池容量(kWh)：'},
 {'id': 'SIP_C_353', 'name': '电机数：'},
 {'id': 'SIP_C_354', 'name': '充电兼容性：'},
 {'id': 'SIP_C_355', 'name': '充电方式：'},
 {'id': 'SIP_C_356', 'name': '快充时间：'},
 {'id': 'SIP_C_357', 'name': '慢充时间：'},
 {'id': 'SIP_C_159', 'name': '驱动方式'},
 {'id': 'SIP_C_160', 'name': '前悬挂类型'},
 {'id': 'SIP_C_161', 'name': '后悬挂类型'},
 {'id': 'SIP_C_162', 'name': '底盘结构'},
 {'id': 'SIP_C_163', 'name': '前轮胎规格'},
 {'id': 'SIP_C_164', 'name': '后轮胎规格'},
 {'id': 'SIP_C_165', 'name': '轮毂材料'},
 {'id': 'SIP_C_166', 'name': '备胎规格'},
 {'id': 'SIP_C_167', 'name': '前制动器类型'},
 {'id': 'SIP_C_168', 'name': '后制动器类型'},
 {'id': 'SIP_C_169', 'name': '驻车制动类型'},
 {'id': 'SIP_C_170', 'name': '分动器类型'},
 {'id': 'SIP_C_171', 'name': '转向助力'},
 {'id': 'SIP_C_172', 'name': '可调悬挂'},
 {'id': 'SIP_C_173', 'name': '空气悬挂'},
 {'id': 'SIP_C_322', 'name': '中央差速器结构'},
 {'id': 'SIP_C_323', 'name': '中央差速器锁止功能'},
 {'id': 'SIP_C_324', 'name': '前桥限滑差速器/差速锁'},
 {'id': 'SIP_C_325', 'name': '后桥限滑差速器/差速锁'},
 {'id': 'SIP_C_177_178', 'name': '主/副驾驶座安全气囊'},
 {'id': 'SIP_C_179_180', 'name': '前/后排侧气囊'},
 {'id': 'SIP_C_181_182', 'name': '前/后头部气帘'},
 {'id': 'SIP_C_183', 'name': '膝部气囊'},
 {'id': 'SIP_C_184', 'name': '安全带未系提示'},
 {'id': 'SIP_C_185', 'name': '自动防抱死(ABS等)'},
 {'id': 'SIP_C_186', 'name': '制动力分配'},
 {'id': 'SIP_C_187', 'name': '刹车辅助'},
 {'id': 'SIP_C_188', 'name': '牵引力控制'},
 {'id': 'SIP_C_189', 'name': '车身稳定控制'},
 {'id': 'SIP_C_190', 'name': '主动刹车/安全系统'},
 {'id': 'SIP_C_191', 'name': '自动驻车'},
 {'id': 'SIP_C_358', 'name': '上坡辅助'},
 {'id': 'SIP_C_192', 'name': '陡坡缓降'},
 {'id': 'SIP_C_193', 'name': '发动机电子防盗'},
 {'id': 'SIP_C_194', 'name': '车内中控锁'},
 {'id': 'SIP_C_195', 'name': '遥控钥匙'},
 {'id': 'SIP_C_196', 'name': '无钥匙启动系统'},
 {'id': 'SIP_C_336', 'name': '无钥匙进入系统：'},
 {'id': 'SIP_C_197', 'name': '胎压监测装置'},
 {'id': 'SIP_C_198', 'name': '零胎压继续行驶'},
 {'id': 'SIP_C_199', 'name': '并线辅助'},
 {'id': 'SIP_C_204', 'name': '全景摄像头'},
 {'id': 'SIP_C_205', 'name': '夜视系统'},
 {'id': 'SIP_C_312', 'name': 'ISO FIX儿童座椅接口：'},
 {'id': 'SIP_C_313', 'name': 'LATCH座椅接口(兼容ISO FIX)：'},
 {'id': 'SIP_C_314', 'name': '儿童安全锁：'},
 {'id': 'SIP_C_316', 'name': '天窗型式：'},
 {'id': 'SIP_C_210', 'name': '运动外观套件'},
 {'id': 'SIP_C_212', 'name': '电动吸合门'},
 {'id': 'SIP_C_337', 'name': '电动后备厢：'},
 {'id': 'SIP_C_338', 'name': '感应后备厢：'},
 {'id': 'SIP_C_339', 'name': '车顶行李架：'},
 {'id': 'SIP_C_300', 'name': '车身其它配置：'},
 {'id': 'SIP_C_213', 'name': '真皮方向盘'},
 {'id': 'SIP_C_214_215', 'name': '方向盘调节'},
 {'id': 'SIP_C_216', 'name': '方向盘电动调节'},
 {'id': 'SIP_C_217', 'name': '多功能方向盘'},
 {'id': 'SIP_C_218', 'name': '方向盘换挡'},
 {'id': 'SIP_C_340', 'name': '方向盘加热：'},
 {'id': 'SIP_C_341', 'name': '方向盘记忆：'},
 {'id': 'SIP_C_342', 'name': '全液晶仪表盘：'},
 {'id': 'SIP_C_175', 'name': '定速巡航'},
 {'id': 'SIP_C_176', 'name': '自适应巡航'},
 {'id': 'SIP_C_219', 'name': '行车电脑显示屏'},
 {'id': 'SIP_C_200', 'name': 'HUD抬头数字显示'},
 {'id': 'SIP_C_343_201', 'name': '前/后倒车雷达'},
 {'id': 'SIP_C_202', 'name': '倒车影像'},
 {'id': 'SIP_C_203', 'name': '自动停车入位'},
 {'id': 'SIP_C_221', 'name': '行李舱灯'},
 {'id': 'SIP_C_222', 'name': '独立电源接口'},
 {'id': 'SIP_C_223', 'name': '中控液晶屏分屏显示'},
 {'id': 'SIP_C_301', 'name': '车内其它配置：'},
 {'id': 'SIP_C_224', 'name': '座椅材质'},
 {'id': 'SIP_C_225', 'name': '运动座椅'},
 {'id': 'SIP_C_226', 'name': '座椅高低调节'},
 {'id': 'SIP_C_227', 'name': '腰部支撑调节'},
 {'id': 'SIP_C_228', 'name': '肩部支撑调节'},
 {'id': 'SIP_C_229_230', 'name': '主/副驾驶座电动调节'},
 {'id': 'SIP_C_317', 'name': '后排座椅调节：'},
 {'id': 'SIP_C_233', 'name': '电动座椅记忆'},
 {'id': 'SIP_C_234_235', 'name': '前/后座椅加热'},
 {'id': 'SIP_C_236_344', 'name': '前/后座椅通风'},
 {'id': 'SIP_C_237_345', 'name': '前/后座椅按摩'},
 {'id': 'SIP_C_238_239', 'name': '后排座椅放倒方式'},
 {'id': 'SIP_C_240', 'name': '第三排座椅'},
 {'id': 'SIP_C_241_242', 'name': '前/后座中央扶手'},
 {'id': 'SIP_C_346', 'name': '后排杯架：'},
 {'id': 'SIP_C_321', 'name': 'CD/DVD：'},
 {'id': 'SIP_C_247', 'name': 'CD支持MP3/WMA'},
 {'id': 'SIP_C_248', 'name': '外接音源接口'},
 {'id': 'SIP_C_249', 'name': '扬声器喇叭数量(个)'},
 {'id': 'SIP_C_250', 'name': '音响品牌'},
 {'id': 'SIP_C_251', 'name': '蓝牙/车载电话'},
 {'id': 'SIP_C_252', 'name': '车载电视'},
 {'id': 'SIP_C_253', 'name': '中控台液晶屏'},
 {'id': 'SIP_C_254', 'name': '后排液晶屏'},
 {'id': 'SIP_C_255', 'name': 'GPS导航系统'},
 {'id': 'SIP_C_257', 'name': '车载信息服务'},
 {'id': 'SIP_C_258', 'name': '人机交互系统'},
 {'id': 'SIP_C_318', 'name': '近光灯：'},
 {'id': 'SIP_C_347', 'name': '远光灯：'},
 {'id': 'SIP_C_260', 'name': '日间行车灯'},
 {'id': 'SIP_C_261', 'name': '前雾灯'},
 {'id': 'SIP_C_262', 'name': '大灯自动开闭'},
 {'id': 'SIP_C_263', 'name': '大灯随动调节'},
 {'id': 'SIP_C_264', 'name': '大灯高度可调'},
 {'id': 'SIP_C_265', 'name': '大灯清洗装置'},
 {'id': 'SIP_C_266', 'name': '车内氛围灯'},
 {'id': 'SIP_C_348', 'name': '自适应远近光：'},
 {'id': 'SIP_C_349', 'name': '转向辅助灯：'},
 {'id': 'SIP_C_267_268', 'name': '前/后电动车窗'},
 {'id': 'SIP_C_269', 'name': '车窗一键功能'},
 {'id': 'SIP_C_270', 'name': '车窗防夹手功能'},
 {'id': 'SIP_C_271', 'name': '防紫外线/隔热玻璃'},
 {'id': 'SIP_C_319_277', 'name': '内/外后视镜防眩目'},
 {'id': 'SIP_C_278', 'name': '后视镜电动调节'},
 {'id': 'SIP_C_279', 'name': '后视镜加热'},
 {'id': 'SIP_C_282', 'name': '后视镜电动折叠'},
 {'id': 'SIP_C_272', 'name': '前感应雨刷'},
 {'id': 'SIP_C_273', 'name': '后雨刷'},
 {'id': 'SIP_C_274', 'name': '后风挡除霜'},
 {'id': 'SIP_C_275', 'name': '后风挡遮阳帘'},
 {'id': 'SIP_C_276', 'name': '后排侧遮阳帘'},
 {'id': 'SIP_C_350', 'name': '后排侧隐私玻璃：'},
 {'id': 'SIP_C_351', 'name': '后视镜记忆：'},
 {'id': 'SIP_C_352', 'name': '遮阳板化妆镜：'},
 {'id': 'SIP_C_320', 'name': '空调'},
 {'id': 'SIP_C_285', 'name': '后排出风口'},
 {'id': 'SIP_C_286', 'name': '前排温度分区控制'},
 {'id': 'SIP_C_287', 'name': '后排独立温区控制'},
 {'id': 'SIP_C_288', 'name': '空气调节/花粉过滤'},
 {'id': 'SIP_C_289', 'name': '车载冰箱'},
 {'id': 'SIP_C_290', 'name': '风冷手套箱'},
 {'id': 'SIP_C_291', 'name': '车身可选颜色'},
 {'id': 'SIP_C_292', 'name': '内饰可选颜色'}]
        carinfor = json.loads(response.body_as_unicode())
        for infordict in infordictlist:
            CARvalue=carinfor.get(infordict.get('id'))
            if CARvalue:
                cardict={}
                #cardict['name']=infordict.get('name')
                #cardict['value']=carinfor.get(infordict.get('id'))
                cardict[infordict.get('name')]=carinfor.get(infordict.get('id'))
                carinfo.append(cardict)
        print(carinfo)



#dict
#In [24]: optionlist = sel.xpath('//table[@id="trimArglist"]/tbody/tr')
#In [44]: for option in optionlist:
#    ...:     optionid = option.xpath('./@id').extract_first()
#    ...:     optionname = option.xpath('./th[@class="th1"]/a/text()').extract_first()
#    ...:     if optionname:
#    ...:         pass
#    ...:     else:
#    ...:         optionname = option.xpath('./th[@class="th1"]/text()').extract_first()
#    ...:     if optionname:
#               optiondict={}
#               optionname=optionname.replace('\xa0', '')
#    ...:       optiondict['id']=optionid
#               optiondict['name']=optionname
#    ...:       optiondictlist.append(optiondict)

    