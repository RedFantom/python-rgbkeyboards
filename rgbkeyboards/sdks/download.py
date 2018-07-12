"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom

This file can be used to automatically download the correct SDK DLL
files from the respective sources, extract them from the ZIP-files and
rename the files so they can immediately be used within the package.
"""
import os
from shutil import rmtree
import sys
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
import zipfile


TARGETS = {
    "Corsair": {
        "link": "http://forum.corsair.com/v3/attachment.php?attachmentid=24542&d=1457043299",
        "files": {
            "CUESDK/bin/x64/CUESDK.x64_2013.dll": "Corsair64.dll",
            "CUESDK/bin/i386/CUESDK_2013.dll": "Corsair.dll",
        }
    },
    "CoolerMaster": {
        "link": "https://makerhub.coolermaster.com/custom-lighting/assets/sdk/coolermaster-sdk.zip",
        "files": {
            "Src/SDK/x64/SDKDLL.dll": "MasterKeys64.dll",
            "Src/SDK/x86/SDKDLL.dll": "MasterKeys.dll",
        }
    },
    "Logitech": {
        "link": "https://www.logitechg.com/sdk/LED_8.87.zip",
        "files": {
            "LED/Lib/LogitechLedEnginesWrapper/x64/LogitechLedEnginesWrapper.dll":
                "Logitech64.dll",
            "LED/Lib/LogitechLedEnginesWrapper/x86/LogitechLedEnginesWrapper.dll":
                "Logitech.dll",
        }
    }
}


DESCRIPTION = \
    "This script can automatically download and extract the DLL files from\n" \
    "the various SDK files for the different back-ends that this library\n" \
    "supports on Windows. If you choose not to download these files, then\n" \
    "downloading manually is required in order to use the back-ends\n" \
    "that depend on their respective SDKs\n\n"


INSTALL = \
    "Would you like to download the SDK DLL files? (y/n) [y]: "


DISCLAIMER = \
    "The SDK DLL files that are required for the various built-in back-ends\n" \
    "on Windows are each covered by its own License. The respective licenses\n" \
    "can be found by downloading the ZIP files for which the links are\n" \
    "present in these files and extracting them. Note that the licenses are\n" \
    "non-transferable, hence the need for this file in the first place.\n\n" \
    "The authors of this file will not accept any responsibility for your\n" \
    "agreement to any of these individual licenses and do not form a party\n" \
    "in the license agreement between you (or the organisation you\n" \
    "represent) and the author of the SDK files.\n\n"

DISCLAIMER_PROMPT = \
    "Do you acknowledge that you have read the disclaimer and agree to\n" \
    "its terms? (y/n) [n] "

FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def printf(string, end="\n"):
    sys.stdout.write(string + end)
    sys.stdout.flush()


if __name__ == '__main__':
    printf(DESCRIPTION)
    a = input(INSTALL)
    if a == "n":
        exit()
    printf(DISCLAIMER)
    a = input(DISCLAIMER_PROMPT)
    if a != "y":
        exit()

    for name, target in TARGETS.items():

        printf("Downloading files for target '{}'... ".format(name), end="")
        file_name = "{}.zip".format(name)
        urlretrieve(target["link"], file_name)
        printf("Done.")

        printf("Extracting files... ", end="")
        with zipfile.ZipFile(file_name, "r") as zip_file:
            for file, target_file in target["files"].items():
                try:
                    zip_file.extract(file, name)
                except KeyError as e:
                    printf("Failed: {}".format(e))
                    break
                src = os.path.join(FILE_DIR, name, file)
                dst = os.path.join(FILE_DIR, target_file)
                os.rename(src, dst)
            if os.path.exists(name):
                rmtree(name)
        os.remove(file_name)
        printf("Done.")
