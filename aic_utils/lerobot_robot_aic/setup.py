#
#  Copyright (C) 2026 Intrinsic Innovation LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# import sys

from setuptools import find_packages, setup

package_name = "lerobot_robot_aic"


# # colcon may call `setup.py develop --uninstall` during editable installs.
# # Newer setuptools no longer supports `--uninstall`, so drop it when present.
# if "develop" in sys.argv and "--uninstall" in sys.argv:
#     sys.argv.remove("--uninstall")
    
# if "develop" in sys.argv and "--build-directory" in sys.argv:
#     sys.argv.remove("--build-directory")
    
# if "develop" in sys.argv and "--editable" in sys.argv:
#     sys.argv.remove("--editable")


setup(
    name=package_name,
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["pyspacemouse", "setuptools"],
    zip_safe=True,
    maintainer="koonpeng",
    maintainer_email="koonpeng@intrinsic.ai",
    entry_points={
        "console_scripts": [],
    },
)