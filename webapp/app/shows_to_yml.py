import database
import yaml
import datetime
import os

def set_output_dir():
    dir = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    os.mkdir(dir)
    os.chdir(dir)
    print(f"Output directory: {os.getcwd()}")

def write_file_for_show(show_slug,band_name):
    show = database.read_show("..",show_slug["id"])

    show['band'] = band_name
    show['show_date'] = show_slug['show_date']
    show['venue'] = show_slug['venue']
    show['setlist'] = show_slug['setlist']
    show['other_bands'] = show_slug['other_bands']
    show['recorded'] = show_slug['recorded']

    fid = show_slug['id']
    print(f"processing {fid}")
    stream = open(f"{fid}.md","w+")
    yaml.dump(show,stream,default_flow_style=False,explicit_start=True,explicit_end=True,default_style='"',width=70)
    stream.close()

def main():
    set_output_dir()



    band_names = ["Slinkees","Teen Idles","Minor Threat","Minor Threat","Minor Threat"]

    bands = ["slinkees","teenidles","minorthreat1","minorthreat2","minorthreat3"]
    # bands = ["slinkees","teenidles"]
    # bands = ["slinkees"]

    for band,band_name in zip(bands,band_names):
        shows = database.read_shows("..",band)
        for show_slug in shows["list"]:
            write_file_for_show(show_slug,band_name)

if __name__== "__main__":
    main()
