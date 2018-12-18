"""
作者： 阿荣苏乙拉

这是 AronNote的Menkcode转Unicode的方法

## convert rule  转化规则

蒙科立编码到UNICODE转换表

根据 [前一个]， [当前]， [下一个] 三个代码判断输出值


convert_rule 格式
1. 序号 优先级
2. 当前字符(代码)的范围
3. 上一个代码的范围
4. 下一个代码的范围
5. 替换的Unicode序列
6. 前进几个，默认(0)的时候前进一个，(1) 前进两个位置

代码范围
1，2，3均为代码范围，

0. 离散的单位
1. 连续的范围
    比如(1, 0xE28B, 0xE28F) 表示从0xE28B到0xE28F（包含）结束的所有字符代码

使用以下规则表动态生成正则表达式
"""

#%%
from collections import defaultdict

import re

MENK_CODE = [1, 0xE264, 0xE34F]


convert_rules = (
    (1, (0, 0x0020), (0,), (1, 0xE235, 0xE239), (0,), 0,),
    (2, (0, 0x0020), (0,), (1, 0xE24E, 0xE252), (0,), 0,),
    (3, (0, 0x0020), (0,), (0, 0xE254, 0xE256, 0xE258, 0xE25A, 0xE25C, 0xE269, 0xE26A, 0xE26B, 0xE274, 0xE275), (0,), 0,),
    (4, (0, 0x0020), (0,), (0, 0xE285, 0xE28D, 0xE289, 0xE28A, 0xE291, 0xE292, 0xE296, 0xE29E, 0xE29F, 0xE2A3, 0xE2AB, 0xE2AC), (0x202F,), 0,),
    (5, (0, 0xE234), (0,), (0,), (0x1800,), 0,),
    (6, (0, 0xE235), (0,), (0,), (0x1801,), 0,),
    (7, (0, 0xE236), (0,), (0,), (0x1802, 0x0020), 0,),
    (8, (0, 0xE237), (0,), (0,), (0x1803, 0x0020), 0,),
    (9, (0, 0xE238), (0,), (0,), (0x1804,), 0,),
    (10, (0, 0xE239), (0,), (0,), (0x1805,), 0,),
    (11, (0, 0xE23A), (0,), (0,), (0x1806,), 0,),
    (12, (0, 0xE23B), (0,), (0,), (0x1807,), 0,),
    (13, (0, 0xE23C), (0,), (0,), (0x1808,), 0,),
    (14, (0, 0xE23D), (0,), (0,), (0x1809,), 0,),
    (15, (0, 0xE23E), (0,), (0,), (0x180A,), 0,),
    (16, (0, 0xE23F), (0,), (0,), (0x1800, 0x180B), 0,),
    (17, (0, 0xE240), (0,), (0,), (0x1800, 0x180C), 0,),
    (18, (0, 0xE241), (0,), (0,), (0x1800, 0x180D), 0,),
    (19, (0, 0xE242), (0,), (0,), (0x1800, 0x200D), 0,),
    (20, (0, 0xE243), (0,), (0,), (0x00B7,), 0,),
    (21, (0, 0xE244), (0,), (0,), (0x1810,), 0,),
    (22, (0, 0xE245), (0,), (0,), (0x1811,), 0,),
    (23, (0, 0xE246), (0,), (0,), (0x1812,), 0,),
    (24, (0, 0xE247), (0,), (0,), (0x1813,), 0,),
    (25, (0, 0xE248), (0,), (0,), (0x1814,), 0,),
    (26, (0, 0xE249), (0,), (0,), (0x1815,), 0,),
    (27, (0, 0xE24A), (0,), (0,), (0x1816,), 0,),
    (28, (0, 0xE24B), (0,), (0,), (0x1817,), 0,),
    (29, (0, 0xE24C), (0,), (0,), (0x1818,), 0,),
    (30, (0, 0xE24D), (0,), (0,), (0x1819,), 0,),
    (31, (0, 0xE24E), (0,), (0,), (0x2048,), 0,),
    (32, (0, 0xE24F), (0,), (0,), (0x2049,), 0,),
    (33, (0, 0xE250), (0,), (0,), (0xFE15,), 0,),
    (34, (0, 0xE251), (0,), (0,), (0xFE16,), 0,),
    (35, (0, 0xE252), (0,), (0,), (0xFE14,), 0,),
    (36, (0, 0xE253), (0,), (0,), (0xFE35,), 0,),
    (37, (0, 0xE254), (0,), (0,), (0xFE36,), 0,),
    (38, (0, 0xE255), (0,), (0, 0xE255), (0xFE3D,), 1,),
    (39, (0, 0xE255), (0,), (0,), (0xFE3F,), 0,),
    (40, (0, 0xE256), (0,), (0, 0xE256), (0xFE3E,), 1,),
    (41, (0, 0xE256), (0,), (0,), (0xFE40,), 0,),
    (42, (0, 0xE257), (0,), (0,), (0xFE47,), 0,),
    (43, (0, 0xE258), (0,), (0,), (0xFE48,), 0,),
    (44, (0, 0xE259), (0,), (0,), (0xFE3D,), 0,),
    (45, (0, 0xE25A), (0,), (0,), (0xFE3E,), 0,),
    (46, (0, 0xE25B), (0,), (0,), (0xFE43,), 0,),
    (47, (0, 0xE25C), (0,), (0,), (0xFE44,), 0,),
    (48, (0, 0xE25D), (0,), (0,), (0xFE10,), 0,),
    (49, (0, 0xE260), (0,), (0,), (0xFE31,), 0,),
    (50, (0, 0xE261), (0,), (0,), (0xFE31,), 0,),
    (51, (0, 0xE263), (0,), (0,  0xE235, 0xE239), (0,), 0,),
    (52, (0, 0xE263), (0,), (0,  0xE24E, 0xE252), (0,), 0,),
    (53, (0, 0xE263), (0,), (0,  0xE254, 0xE256, 0xE258, 0xE25A, 0xE25C, 0xE269, 0xE26A, 0xE26B, 0xE274, 0xE275), (0,), 0,),
    (54, (0, 0xE263), (0,), (0,  0xE289, 0xE28A, 0xE291, 0xE292, 0xE29E, 0xE29F, 0xE2AB, 0xE2AC, 0xE285, 0xE28D, 0xE296, 0xE2A3, 0xE321), (0x202F,), 0,),
    (55, (0, 0xE263), (0,), (0,), (0x202F,), 0,),
    (56, (0, 0xE264), (0,), (0,), (0x1820,), 0,),
    (57, (0, 0xE265), (0,), (0,), (0x1820, 0x180B), 0,),
    (58, (0, 0xE266), (0,), (0,), (0x1820,), 0,),
    (59, (0, 0xE267), (0,), (0, 0xE26C, 0xE26D), (0x1820,), 1,),
    (60, (0, 0xE267), (0,), (0, 0xE27E), (0x1822,), 0,),
    (61, (0, 0xE267), (0,), (0, 0xE289), (0x1823,), 1,),
    (62, (0, 0xE267), (0,), (0, 0xE291), (0x1824,), 1,),
    (63, (0, 0xE267), (0,), (0, 0xE29E), (0x1825,), 1,),
    (64, (0, 0xE267), (0,), (0, 0xE2AB), (0x1826,), 1,),
    (65, (0, 0xE267), (0,), (0,), (0x1821,), 0,),
    (66, (1, 0xE268, 0xE269), (0,), (0,), (0x1820,), 0,),
    (67, (0, 0xE26A), (0,), (0,), (0x180E, 0x1820), 0,),
    (68, (0, 0xE26B), (0,), (0,), (0x1820,), 0,),
    (69, (0, 0xE26C, 0xE26D), (0,), MENK_CODE, (0x1820,), 0,),
    (70, (0, 0xE26C, 0xE26D), (0,), (0,), (0x1820, 0x180A), 0,),
    (71, (0, 0xE26E, 0xE26F), (0,), (0,), (0x1820,), 0,),
    (72, (0, 0xE270, 0xE271), (0,), (0,), (0x1821,), 0,),
    (73, (0, 0xE272), (0,), (0,), (0x1821, 0x180B), 0,),
    (74, (0, 0xE273), (0,), (0,), (0x1821,), 0,),
    (75, (0, 0xE274), (0,), (0,), (0x180E, 0x1821), 0,),
    (76, (0, 0xE275), (0,), (0,), (0x1821,), 0,),
    (77, (0, 0xE276), (0, 0xE266, 0xE26C, 0xE271, 0xE276, 0xE27A, 0xE27E, 0xE284, 0xE289, 0xE28C, 0xE291, 0xE295, 0xE29B, 0xE29C, 0xE29D, 0xE29E, 0xE2A2, 0xE2A8, 0xE2A9, 0xE2AA, 0xE2AB), (0, 0xE2EB, 0xE2EE, 0xE2EF, 0xE2F0), (0x1829,), 1,),
    (78, (0, 0xE276), (0,), (0,), (0x1821,), 0,),
    (79, (1, 0xE277, 0xE278), (0,), (0,), (0x1821,), 0,),
    (80, (1, 0xE279, 0xE27B), (0,), (0,), (0x1822,), 0,),
    (81, (0, 0xE27C), (0,), (0, 0xE26A, 0xE274), (0x1836,), 0,),
    (82, (0, 0xE27C), (0,), (0,), (0x1822,), 0,),
    (83, (0, 0xE27D), (0,), (0,), (0x1822, 0x180B), 0,),
    (84, (0, 0xE27E), (0,), (0, 0xE27E), (0x1822,), 1,),
    (85, (0, 0xE27E), (0,), (0,), (0x1822,), 0,),
    (86, (0, 0xE282), (0, 0x0020), (0, 0x0020), (0x202f, 0x1822, 0x180B), 1,),
    (86, (1, 0xE27F, 0xE282), (0,), (0,), (0x1822,), 0,),
    (87, (1, 0xE283, 0xE284), (0,), (0,), (0x1823,), 0,),
    (88, (0, 0xE285), (0, 0xE263, 0x0020), (0,), (0x1824, 0x180B, 0x0020), 1,),
    (89, (0, 0xE285), (0,), (0,), (0x1823,), 0,),
    (90, (0, 0xE286), (0,), MENK_CODE, (0x1823,), 0,),
    (91, (0, 0xE286), (0,), (0,), (0x1823, 0x180B), 0,),
    (92, (0, 0xE287), (0,), (0,), (0x1823,), 0,),
    (93, (0, 0xE288), (0,), (0,), (0x1823, 0x180B), 0,),
    (94, (0, 0xE289), (0, 0xE263, 0x0020), (0, 0xe2b5), (0x1824, 0x180B), 0,),
    (94, (0, 0xE289), (0, 0xE263, 0x0020), (0,), (0x1824,), 0,),
    (95, (0, 0xE289), (0,), (0, 0xE26C, 0xE276), (0x1833,), 1,),
    (96, (0, 0xE289), (0,), (0,), (0x1823,), 0,),
    (97, (0, 0xE28A), (0,), (0,), (0x1823,), 0,),
    (98, (0, 0xE28D), (0, 0x0020), (0, 0x0020), (0x1824, 0x180B), 0,),
    (98, (1, 0xE28B, 0xE28F), (0,), (0,), (0x1824,), 0,),
    (99, (0, 0xE290), (0,), (0,), (0x1824, 0x180B), 0,),
    (100, (0, 0xE291), (0,), (0, 0xE26C, 0xE276), (0x1833,), 1,),
    (101, (0, 0xE291), (0,), (0,), (0x1824,), 0,),
    (102, (0, 0xE292), (0,), (0,), (0x1824,), 0,),
    (103, (0, 0xE293), (0,), (0,), (0x1825,), 0,),
    (104, (0, 0xE294), (0,), (0,), (0x1825, 0x180B), 0,),
    (104, (0, 0xE296), (0, 0x0020), (0, 0x0020), (0x1825, 0x180B), 0,),
    (105, (1, 0xE295, 0xE29A), (0,), (0,), (0x1825,), 0,),
    (106, (0, 0xE29B), (0,), (0,), (0x1825, 0x180C), 0,),
    (107, (1, 0xE29C, 0xE29F), (0,), (0,), (0x1825,), 0,),
    (108, (0, 0xE2A0), (0,), (0,), (0x1826,), 0,),
    (109, (0, 0xE2A1), (0,), (0,), (0x1826, 0x180B), 0,),
    (110, (1, 0xE2A2, 0xE2A7), (0,), (0,), (0x1826,), 0,),
    (111, (0, 0xE2A8), (0,), (0,), (0x1826, 0x180C), 0,),
    (112, (1, 0xE2A9, 0xE2AA), (0,), (0,), (0x1826,), 0,),
    (113, (0, 0xE2AB), (0,), (0, 0xE321), (0x1826, 0x180B), 1,),
    (114, (0, 0xE2AB), (0,), (0,), (0x1826,), 0,),
    (115, (0, 0xE2AC), (0,), (0,), (0x1826,), 0,),
    (116, (1, 0xE2AD, 0xE2B0), (0,), (0,), (0x1827,), 0,),
    (117, (1, 0xE2B1, 0xE2BA), (0,), (0,), (0x1828,), 0,),
    (118, (1, 0xE2BB, 0xE2BE), (0,), (0,), (0x1829,), 0,),
    (119, (0, 0xE2BF), (0,), (0,), (0x1828,), 0,),
    (120, (0, 0xE2C0), (0,), (0, 0xE2E8, 0xE2EF, 0xE2F0), (0x1829,), 1,),
    (121, (0, 0xE2C0), (0,), (0,), (0x1828,), 0,),
    (122, (1, 0xE2C1, 0xE2C7), (0,), (0,), (0x182A,), 0,),
    (123, (1, 0xE2C8, 0xE2CD), (0,), (0,), (0x182B,), 0,),
    (124, (0, 0xE2CE), (0,), (0,), (0x182C,), 0,),
    (125, (0, 0xE2CF), (0,), (0,), (0x182D,), 0,),
    (126, (1, 0xE2D0, 0xE2D7), (0,), (0,), (0x182C,), 0,),
    (127, (0, 0xE2D8), (0,), (0, 0xE26C, 0xE26D, 0xE26F, 0xE276, 0xE277, 0xE278, 0xE285, 0xE286, 0xE287, 0xE289, 0xE28D, 0xE28E, 0xE28F, 0xE291, 0xE292), (0x182C,), 0,),
    (128, (0, 0xE2D8), (0,), (0,), (0x182D,), 0,),
    (129, (1, 0xE2D9, 0xE2DB), (0,), (0,), (0x182D,), 0,),
    (130, (0, 0xE2DC), (0,), (0, 0xE26C, 0xE26D, 0xE26F, 0xE276, 0xE277, 0xE278, 0xE285, 0xE286, 0xE287, 0xE289, 0xE28D, 0xE28E, 0xE28F, 0xE291, 0xE292), (0x182C,), 0,),
    (131, (0, 0xE2DC), (0,), (0,), (0x182D,), 0,),
    (132, (1, 0xE2DD, 0xE2E0), (0,), (0,), (0x182C,), 0,),
    (133, (1, 0xE2E1, 0xE2ED), (0,), (0,), (0x182D,), 0,),
    (134, (0, 0xE2EE), (0,), (0, 0xE26C, 0xE26D, 0xE26F, 0xE276, 0xE277, 0xE278, 0xE285, 0xE286, 0xE287, 0xE289, 0xE28D, 0xE28E, 0xE28F, 0xE291, 0xE292), (0x182C,), 0,),
    (135, (0, 0xE2EE), (0,), (0,), (0x182D,), 0,),
    (136, (1, 0xE2EF, 0xE2F0), (0,), (0,), (0x182D,), 0,),
    (137, (1, 0xE2F1, 0xE2F6), (0,), (0,), (0x182E,), 0,),
    (138, (1, 0xE2F7, 0xE2FC), (0,), (0,), (0x182F,), 0,),
    (139, (1, 0xE2FD, 0xE302), (0,), (0,), (0x1830,), 0,),
    (140, (1, 0xE303, 0xE307), (0,), (0,), (0x1831,), 0,),
    (141, (1, 0xE308, 0xE30A), (0,), (0,), (0x1832,), 0,),
    (142, (0, 0xE30B), MENK_CODE, (0,), (0x1832,), 0,),
    (143, (0, 0xE30B), (0,), (0,), (0x1833, 0x180B), 0,),
    (144, (0, 0xE30C), (0,), (0,), (0x1832, 0x180B), 0,),
    (145, (1, 0xE30D, 0xE30E), (0,), (0,), (0x1832,), 0,),
    (146, (0, 0xE30F), (0,), (0,), (0x1833,), 0,),
    (147, (0, 0xE310), MENK_CODE, (0,), (0x1833,), 0,),
    (148, (0, 0xE310), (0,), (0,), (0x1833, 0x180B), 0,),
    (149, (0, 0xE311), (0,), (0,), (0x1833,), 0,),
    (150, (0, 0xE312), (0,), (0,), (0x1833, 0x180B), 0,),
    (151, (0, 0xE313), MENK_CODE, (0,), (0x1833,), 0,),
    (152, (0, 0xE313), (0,), (0,), (0x1833, 0x180B), 0,),
    (153, (0, 0xE314), (0,), (0,), (0x1833,), 0,),
    (154, (1, 0xE315, 0xE317), (0,), (0,), (0x1834,), 0,),
    (155, (1, 0xE318, 0xE31D), (0,), (0,), (0x1835,), 0,),
    (156, (0, 0xE321), (0,), (0, 0xe27b), (0x1836, 0x180B), 0,),
    (156, (1, 0xE31E, 0xE321), (0,), (0, 0xe27e), (0x1836, 0x180B), 0,),
    (156, (1, 0xE31E, 0xE321), (0,), (0,), (0x1836,), 0,),
    (157, (1, 0xE322, 0xE328), (0,), (0,), (0x1837,), 0,),
    (158, (1, 0xE329, 0xE32B), (0,), (0,), (0x1838,), 0,),
    (159, (0, 0xE32C), (0, 0xE2EF), (0,), (0x1827,), 0,),
    (160, (0, 0xE32C), (0,), (0,), (0x1838,), 0,),
    (161, (1, 0xE32D, 0xE332), (0,), (0,), (0x1839,), 0,),
    (162, (1, 0xE333, 0xE338), (0,), (0,), (0x183A,), 0,),
    (163, (1, 0xE339, 0xE33E), (0,), (0,), (0x183B,), 0,),
    (164, (1, 0xE33F, 0xE341), (0,), (0,), (0x183C,), 0,),
    (165, (1, 0xE342, 0xE344), (0,), (0,), (0x183D,), 0,),
    (166, (1, 0xE345, 0xE347), (0,), (0,), (0x183E,), 0,),
    (167, (1, 0xE348, 0xE34A), (0,), (0,), (0x183F,), 0,),
    (168, (1, 0xE34B, 0xE34D), (0,), (0,), (0x1840,), 0,),
    (169, (0, 0xE34E), (0,), (0,), (0x1841,), 0,),
    (170, (0, 0xE34F), (0,), (0,), (0x1842,), 0,)
)


#%%
def compile_coderange(coderange):
    """
    将代码范围转换成用正则表达式
    """
    assert coderange[0] in [0, 1]

    if len(coderange) > 1:

        # 连续的代码
        if coderange[0] == 1:
            return r"[%s-%s]" % (chr(coderange[1]), chr(coderange[2]))

        # 离散的代码
        else:
            # 有多个字符的话应该用方括号括起来
            if len(coderange) > 2:
                return r"[%s]" % ("".join([chr(ch) for ch in coderange[1:]]))
            # 只有一个字符的话，直接返回
            else:
                return chr(coderange[1])
    else:
        assert coderange[0] == 0
        return "."


def compile_rules():
    ch_repl_dict = defaultdict(lambda: list())
    for i, item in enumerate(convert_rules):
        try:
            assert len(item) == 6
        except:
            print("#"*100)
            print(i)
            raise Exception()
        ptrn = "%s%s%s" % (
            compile_coderange(item[2]),
            compile_coderange(item[1]),
            compile_coderange(item[3])
        )

        repl = None
        if item[4][0] != 0:
            repl = "".join([chr(code) for code in item[4]])

        current_code_range = item[1]

        priority = item[0]

        if current_code_range[0] == 0:
            # 当前字符离散
            for ch in current_code_range[1:]:
                ch_repl_dict[chr(ch)].append([priority, ptrn, repl, item[5]])

        else:
            # 当前字符连续
            for ch in range(current_code_range[1], current_code_range[2]+1):
                ch_repl_dict[chr(ch)].append([priority, ptrn, repl, item[5]])

    ch_repl_dict2 = defaultdict(lambda: list())
    for k, v in ch_repl_dict.items():
        ch_repl_dict2[k] = [
            (re.compile(ptrn), repl, look_ahead) for (_, ptrn, repl, look_ahead) in sorted(v, key=lambda x: x[0])
        ]
    return ch_repl_dict2


replace_rule_dict = compile_rules()

# for k, v in replace_rule_dict.items():
#     print("_"*50)
#     print(k, hex(ord(k)))
#     for (ptrn, repl) in v:
#         # assert repl is not None
#         print("ptrn:", ptrn)
#         print("repl:", repl)


def __convert2unicode_aron(text_m):
    text_u = []
    text_m = "_%s_" % (text_m)
    last_look_ahead = 0
    error_list = []
    for i in range(1, len(text_m)-1):
        if last_look_ahead:
            last_look_ahead = 0
            continue
#         print(i)
        sub_text = text_m[max(0, i-1): min(len(text_m), i+2)]
        for (ptrn, repl, look_ahead) in replace_rule_dict[sub_text[1]]:
            # print("&"*10)
            pp1 = (ptrn, repl)
            # print(ptrn)
            m = ptrn.match(sub_text)
            if m and repl:
#                 print(repl)
                text_u += repl
                last_look_ahead = look_ahead
                break
            else:
                pass
        else:
            text_u += sub_text[1]
            if sub_text[1] != " ":
                error_list += sub_text[1]
    return "".join(text_u), error_list


def convert2unicode_aron(text_m):
    text_u = []
    for line in re.split('\r?\n', text_m):
        text_u_sub, _ = __convert2unicode_aron(line)
        text_u.append(text_u_sub)
    return "\n".join(text_u)


if __name__ == '__main__':
    # text_m = '  '
    # print([hex(ord(ch)) for ch in text_m])
    # text_u, e = __convert2unicode_aron(text_m)
    # print([hex(ord(ch)) for ch in text_u])

    # print(text_u)
    # print(e)


    # print(convert2unicode_aron("\ue251\n"))

    print(convert2unicode_aron(" "))
