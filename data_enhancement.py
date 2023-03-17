
import xml.etree.ElementTree as ET
import os
import imgaug as ia
import numpy as np
import shutil
from tqdm import tqdm
from PIL import Image
from imgaug import augmenters as iaa
from imgaug import parameters as iap

# 原图片存放路径
img_path    = "C:/Users/Czhannb/Desktop/preimg"
# img_path    = "C:/Users/J.J.Nichoals/Desktop/VOC2007/error/error_JPEGImages/"
# 原xml文件存放路径
xml_path    = "C:/Users/Czhannb/Desktop/prexml"
# xml_path    = "C:/Users/J.J.Nichoals/Desktop/VOC2007/error/error_Annotations/"
# 数据增强后图片的导出路径
imgout_path = "C:/Users/Czhannb/Desktop/postimg"
# imgout_path = "C:/Users/J.J.Nichoals/Desktop/VOC2007/error/result/"
# 数据增强后xml的导出路径
xmlout_path = "C:/Users/Czhannb/Desktop/postxml"
# xmlout_path = "C:/Users/J.J.Nichoals/Desktop/VOC2007/error/result/"

ia.seed(1)

# --------------------------------------------------------------------------------------------------------------------- #
"""             读取xml文件             """
# --------------------------------------------------------------------------------------------------------------------- #
def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id), encoding="utf-8")
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    if root.find('object'):
        for object in root.findall('object'):  # 找到root节点下的所有country节点
            bndbox = object.find('bndbox')  # 子节点下节点rank的值
            xmin = float(bndbox.find('xmin').text)
            xmax = float(bndbox.find('xmax').text)
            ymin = float(bndbox.find('ymin').text)
            ymax = float(bndbox.find('ymax').text)
            # print(xmin,ymin,xmax,ymax)
            bndboxlist.append([xmin, ymin, xmax, ymax])
            # print(bndboxlist)

        bndbox = root.find('object').find('bndbox')
        return bndboxlist
    else:
        return bndboxlist.append([])




# --------------------------------------------------------------------------------------------------------------------- #
"""             解析xml文件             """
# --------------------------------------------------------------------------------------------------------------------- #
def change_xml_list_annotation(root, image_id, new_target, saveroot, id):
    in_file = open(os.path.join(root, str(image_id) + '.xml'), encoding="utf-8")  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    # 修改增强后的xml文件中的filename
    elem = tree.find('filename')
    elem.text = (str(id) + '.jpg')
    xmlroot = tree.getroot()
    # 修改增强后的xml文件中的path
    elem = tree.find('path')
    if elem != None:
        elem.text = (saveroot + str(id) + '.jpg')

    index = 0
    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, str(id + '.xml')))


# --------------------------------------------------------------------------------------------------------------------- #
"""         创建新文件夹          """
# --------------------------------------------------------------------------------------------------------------------- #
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


if __name__ == "__main__":

    IMG_DIR = img_path
    XML_DIR = xml_path

    AUG_XML_DIR = xmlout_path  # 存储增强后的XML文件夹路径
    try:
        shutil.rmtree(AUG_XML_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_XML_DIR)

    AUG_IMG_DIR = imgout_path  # 存储增强后的影像文件夹路径
    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP = 5  # 每张影像增强的数量

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    # 影像增强
    # ---------------------------- 原来的 -------------------------------------------------------------------- #
    # seq = iaa.Sequential([
    #     iaa.Invert(0.5),
    #     iaa.Fliplr(0.5),  # 镜像
    #     iaa.Multiply((1.2, 1.5)),  # change brightness, doesn't affect BBs
    #     iaa.GaussianBlur(sigma=(0, 0.1)),  # iaa.GaussianBlur(0.5),   # 通过sigma模糊每个图像，其中sigma从统一范围[0.0, 1.0)中采样
    #     iaa.Affine(
    #         translate_px={"x": 15, "y": 15},
    #         scale=(0.8, 0.95),
    #     )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
    # ])
    # -------------- 修改 --------------------- #
    seq = iaa.Sequential([
        # 将对比度提高到 100%（被选中的几率为 50%）或 150%（被选中的几率为 30%）或 300%（被选中的几率为 20%）
        iaa.ContrastNormalization(
            iap.Choice(
                [1.0, 1.1, 1.5, 1.3],
                p=[0.1, 0.1, 0.7, 0.1]
            ),
            # iap.Normal(0, 1)
        ),
        iaa.Invert(0.5),           # 反色


        # 将每个图像旋转随机度数，其中度数是从正态分布N(0, 30)中采样的。大多数值将在-60到60的范围内
        iaa.Affine(
            rotate=iap.Normal(0.0, 360),
            translate_px=iap.RandomSign(iap.Poisson(3))
        ),

        # # 向每个像素添加一个随机值，该值是从 beta 分布Beta(0.5, 0.5)中采样的。此分布的峰值在 0.0 和 1.0 附近。
        # # 我们将其乘以 2 并减去 1 以使其进入范围[-1, 1]。然后我们乘以 64 得到范围[-64, 64]。由于我们的 beta 分布是连续的，
        # # 我们将其转换为离散分布。结果是许多像素强度移动了 -64 或 64（或非常接近这两者的值）。其他一些像素强度（大部分）保持在其旧值。
        iaa.AddElementwise(
            iap.Discretize(
                (iap.Beta(0.5, 0.5) * 2 - 1.0) * 16
            )
        ),

        # 使用乘法使每个图像更亮。亮度增加是从正态分布中采样的，转换为只有正值。因此，大多数值预计在0.0到0.2范围内。
        # 添加1.0将亮度设置为1.0 (100%) 到1.2 (120%)。
        iaa.Multiply(
            iap.Positive(iap.Normal(0.0, 0.1)) + 1.1
        )

    ]
    )
    # params = [
    #     iap.Normal(0, 1),
    #     iap.Normal(5, 3),
    #     iap.Normal(iap.Choice([-3, 3]), 1),
    #     iap.Normal(iap.Uniform(-3, 3), 1)
    # ]
    # iap.show_distributions_grid(params)



    for name in tqdm(os.listdir(XML_DIR), desc='Processing'):

        bndbox = read_xml_annotation(XML_DIR, name)

        # 保存原xml文件
        shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)
        # 保存原图
        og_img = Image.open(IMG_DIR + '/' + name[:-4] + '.jpg')
        og_img.convert('RGB').save(AUG_IMG_DIR + name[:-4] + '.jpg', 'JPEG')
        og_xml = open(os.path.join(XML_DIR, name), encoding="utf-8")
        tree = ET.parse(og_xml)
        # 修改增强后的xml文件中的filename
        elem = tree.find('filename')
        elem.text = (name[:-4] + '.jpg')
        tree.write(os.path.join(AUG_XML_DIR, name))

        for epoch in range(AUGLOOP):
            seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
            # 读取图片
            img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
            # sp = img.size
            img = np.asarray(img)
            # bndbox 坐标增强
            for i in range(len(bndbox)):
                bbs = ia.BoundingBoxesOnImage([
                    ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                ], shape=img.shape)

                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                boxes_img_aug_list.append(bbs_aug)

                # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                if n_x1 == 1 and n_x1 == n_x2:
                    n_x2 += 1
                if n_y1 == 1 and n_y2 == n_y1:
                    n_y2 += 1
                if n_x1 >= n_x2 or n_y1 >= n_y2:
                    print('error', name)
                new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])
            # 存储变化后的图片
            image_aug = seq_det.augment_images([img])[0]
            path = os.path.join(AUG_IMG_DIR,
                                str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            image_auged = bbs.draw_on_image(image_aug, size=0)
            Image.fromarray(image_auged).convert('RGB').save(path)

            # 存储变化后的XML
            change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                       str(name[:-4]) + '_' + str(epoch))
            # print(str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            new_bndbox_list = []
    print('Finish!')
