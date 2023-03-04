import cv2
import argparse
import os.path as pth


class Args:
    def __init__(self, ptarget_path, plogo_path):
        self.target_path = ptarget_path
        self.logo_path = plogo_path
        self.prps = WMarkProps()


class WMarkProps:
    def __init__(self, iniCount=1):
        self.count = iniCount


class NotValidAspectRatio(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return "Not valid Aspect ratio"


def LoadParseArgs():
    ap = argparse.ArgumentParser(prog="Water mark adder", add_help=True, exit_on_error=True,
                                 description="This software helps you to add watermark to images")
    ap.add_argument("-tp", "--target-path", required=True,
                    help="Target path for the image for which we need to add logo")
    ap.add_argument("-lp", "--logo-path", required=True, help="Logo path")
    args = ap.parse_args()

    return vars(args)


def CheckExistence(filePath):
    if not pth.exists(filePath):
        raise FileNotFoundError()


def CheckAspectRatio(ratio1, ratio2):
    if abs(ratio1-ratio2) <= 0.1:
        return True
    else:
        return False


def GetAspectRatio(imageContent):
    # height / width
    x, y, _ = imageContent.shape
    return float(x)/y


def DefineShape(imageContent, prefix):
    h, w, _ = imageContent.shape
    print("{2:<10} => Height {0} Width {1}".format(h, w, prefix))


if __name__ == "__main__":
    args = LoadParseArgs()

    target_path = args["target_path"]
    logo_path = args["logo_path"]

    CheckExistence(target_path)
    CheckExistence(logo_path)

    target_content = cv2.imread(filename=target_path, flags=1)
    logo_content = cv2.imread(filename=logo_path, flags=1)

    ratio1 = GetAspectRatio(target_content)
    ratio2 = GetAspectRatio(logo_content)

    tar_hgt, tar_wdt, _ = target_content.shape
    logo_hgt, logo_wdt, _ = logo_content.shape

    # if not CheckAspectRatio(ratio1=ratio1, ratio2=ratio2):
    #     logo_content = cv2.resize(
    #         logo_content, (int(tar_wdt * 0.3), int(ratio2 * tar_wdt * 0.3)))

    print("Aspect Ratio\n{0:<10} {1}\n{2:<10} {3}".format(
        "target", GetAspectRatio(target_content), "logo", GetAspectRatio(logo_content)))

    DefineShape(target_content, prefix="Target")
    DefineShape(logo_content, prefix="Logo")

    cv2.imshow(mat=target_content, winname="target_path")
    cv2.imshow(mat=logo_content, winname="logo_path")

    cv2.waitKey(1000*1)
    cv2.destroyAllWindows()

    centre_x = tar_wdt / 2
    centre_y = tar_hgt / 2
    top_x, top_y = int(centre_x - (logo_wdt/2)), int(centre_y - (logo_hgt/2))
    bottom_x, bottom_y = int(centre_x + (logo_wdt/2)), int(centre_y + (logo_hgt/2))

    res = cv2.addWeighted(target_content[top_y:bottom_y,top_x:bottom_x],0.5,logo_content,0.5,1)
    target_content[top_y:bottom_y,top_x:bottom_x] = res
    
    cv2.imshow(mat=target_content,winname="Watermarked image")
    cv2.imwrite(filename="{0}_{1}.png".format("target","logo"),img=target_content)

    cv2.waitKey(1000*5)
    cv2.destroyAllWindows()
