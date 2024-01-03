import os
from datetime import datetime

available_licences = {
    "MIT": "MIT",
    "GPL-2": "GPL-2.0-only",
    "GPL-3":"GPL-3.0-only",
    "AGPL-3": "AGPL-3.0-only",
    "Apache 2": "Apache-2.0",
    "BSD-2": "BSD-2-Clause",
    "BSD-3": "BSD-3-Clause",
    "BSD-4": "BSD-4-Clause",
    "EPL-1": "EPL-1.0",
    "EPL-2": "EPL-2.0",
    "MPL-1": "MPL-1.0",
    "MPL-1.1": "MPL-1.1",
    "MPL-2": "MPL-2.0",
}


def main():
    app_id = input("Enter your app ID (e.g. com.example.myapp): ")
    while "." not in app_id:
        app_id = input("Enter your app ID (e.g. com.example.myapp): ")


    file_to_create = f"./{app_id}.metainfo.xml"
    if os.path.exists(file_to_create):
        print(file_to_create, "exists already, this script will output to", f"{file_to_create}.1")
        file_to_create += ".1"
    
    user_name = input("Enter your name: ")
    app_name = input("Enter the application name: ")
    licences = ("MIT", "GPL-2", "GPL-3", "AGPL-3", "Apache 2", "BSD-2", "BSD-3", "BSD-4", "EPL-1", "EPL-2", "MPL-1", "MPL-1.1", "MPL-2", "Other")
    print("Choose a License")
    licence_options = ""
    for idx, lic in enumerate(licences):
        licence_options += f"{idx}) {lic}\n"

    print(licence_options)

    while True:
        licence_index = input("Choice: ")
        try:
            licence_index_int = int(licence_index)
        except ValueError:
            licence_index = input("Choice: ")
        else:
            if licence_index_int >= 0 and licence_index_int < len(licences):
                break

    if licences[licence_index_int] == "Other":
        licence_choice = input("Enter your choice of License (See https://spdx.org/licenses/): ")
    else:
        licence_choice = available_licences[licences[licence_index_int]]

    homepage = input("Enter your app's homepage (leave blank to skip): ")
    summary = input("Enter a 1-line summary of your application: ")

    long_desc = input("Enter a detailed description of your application. Press Enter/Return to start a new paragraph. Type DONE when finished: ")
    while True:
        next_para = input("Continue (type DONE when finished): ")
        if next_para.strip() == "DONE":
            break
        else:
            long_desc += f"\n{next_para}"

    screenshots = {}
    while True:
        screenshot = input("Enter the URL of a screenshot of your application: ")
        caption = input("Enter a caption for this screenshot: ")

        screenshots[screenshot] = caption

        more = input("Add another screenshot? [y/N]: ")
        if more.strip() not in ('y', 'Y', 'yes', 'Yes', 'YES'):
            break

    version = input("Enter the version of your application (e.g. 1.0.0): ")

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_year = datetime.now().year

    file_contents = f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright {current_year} {user_name} -->
<component type="desktop-application">
  <id>{app_id}</id>
  <name>{app_name}</name>
  <developer_name>{user_name}</developer_name>
  <launchable type="desktop-id">{app_id}.desktop</launchable>
  <summary>{summary}</summary>
  <description>\n"""

    for paragraph in long_desc.split("\n"):
        file_contents += f"    <p>{paragraph}</p>\n"

    file_contents += "  </description>\n"

    file_contents += f"""
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>{licence_choice}</project_license>

  <!-- Please paste out your OARS content rating below this line -->

  <releases>
    <release version="{version}" date="{current_date}"/>
  </releases>\n"""

    if homepage:
        file_contents += f'\n  <url type="homepage">{homepage}</url>\n'

    file_contents += "\n  <screenshots>\n"

    for url, caption in screenshots.items():
        file_contents += f"""    <screenshot>
      <caption>{caption}</caption>
      <image>{url}</image>
    </screenshot>"""

    file_contents += "\n  </screenshots>\n</component>"

    with open(file_to_create, "w") as f:
        f.write(file_contents)

    print("")
    print(f"AppData Created at {file_to_create}")
    print("You now need to obtain your OARS information and place it in the generated file.")
    print("Please visit https://hughsie.github.io/oars/generate.html to obtain your OARS information.")
    print("")
    print("Exiting")

if __name__ == "__main__":
    main()
