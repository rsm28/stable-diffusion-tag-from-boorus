import re, json
import traceback
import gradio as gr
import requests
from pybooru import Danbooru
from e621 import E621


from modules import script_callbacks, scripts, shared
from modules import generation_parameters_copypaste as parameters_copypaste
from modules.shared import opts


def load_config():
    try:
        with open(
            "extensions\stable-diffusion-tag-from-boorus\ext_config.json", "r"
        ) as f:
            config = json.load(f)
            BLACKLIST = config["BLACKLIST"].split(", ")
            LORA_CLOTHING_BLACKLIST = config["LORA_CLOTHING_BLACKLIST"].split(", ")
            LORA_POSE_BLACKLIST = config["LORA_POSE_BLACKLIST"].split(", ")
            LORA_MISC_BLACKLIST = config["LORA_MISC_BLACKLIST"].split(", ")

        return (
            BLACKLIST,
            LORA_CLOTHING_BLACKLIST,
            LORA_POSE_BLACKLIST,
            LORA_MISC_BLACKLIST,
        )
    except:
        print("An error occurred while loading ext_config.json")
        traceback.print_exc()
        return None


def getTags(
    post_link,
    lora_option,
    dbusername_,
    dbapi_key_,
    e621username_,
    e621api_key_,
    nai_option,
    booru_choice,
):

    (
        BLACKLIST,
        LORA_CLOTHING_BLACKLIST,
        LORA_POSE_BLACKLIST,
        LORA_MISC_BLACKLIST,
    ) = load_config()

    BLACKLIST = dict.fromkeys(BLACKLIST, None)
    LORA_CLOTHING_BLACKLIST = dict.fromkeys(LORA_CLOTHING_BLACKLIST, None)
    LORA_POSE_BLACKLIST = dict.fromkeys(LORA_POSE_BLACKLIST, None)
    LORA_MISC_BLACKLIST = dict.fromkeys(LORA_MISC_BLACKLIST, None)

    if booru_choice == "Danbooru":
        match = re.findall(r"\d+", post_link)
        post_id = match[0]

        client = Danbooru("danbooru", username=dbusername_, api_key=dbapi_key_)
        post = client.post_show(post_id)

        general_tags = post["tag_string_general"]
        character_tags = post["tag_string_character"]
        character_tags = re.sub(r"[()]", r"\\\g<0>", character_tags)

        general_tags = re.sub(r"[()]", r"\\\g<0>", general_tags)
        general_tags = general_tags.replace(" ", ", ")
        general_tags = general_tags.replace("_", " ")
    elif booru_choice == "Safebooru":
        match = re.findall(r"\d+", post_link)
        post_id = match[0]

        response = requests.get(
            f"https://safebooru.org/index.php?page=dapi&s=post&q=index&id={post_id}&json=1"
        )
        general_tags = response.json()[0]["tags"]  # string
        general_tags = re.sub(r"[()]", r"\\\g<0>", general_tags)
        general_tags = general_tags.replace(" ", ", ")
        general_tags = general_tags.replace("_", " ")

        character_tags = ""

    # elif booru_choice == "e621":
    #     match = re.findall(r"\d+", post_link)
    #     post_id = int(match[1])

    #     api = E621((e621username_, e621api_key_))
    #     post = api.posts.get(post_id)

    #     tags = post.tags
    #     general_tag_list = tags.general
    #     species_list = tags.species

    #     general_tag_list += species_list
    #     general_tags = ", ".join(general_tag_list)
    #     general_tags = re.sub(r"[()]", r"\\\g<0>", general_tags)
    #     general_tags = general_tags.replace("_", " ")
    #     character_tags = ""

    character_tags = character_tags.split(" ")[0]
    if lora_option == True:
        character_tags = ""
    else:
        character_tags = "(" + character_tags + ":1.1),"

    if character_tags == "(:1.1),":
        character_tags = ""
    character_tags = character_tags.replace("_", " ")

    try:
        for tag in general_tags.split(", "):
            if tag in BLACKLIST:
                print(f"tag: {tag}")
                general_tags = general_tags.replace(tag, "")
                print("removed tag")

            if lora_option == True:
                if (
                    tag in LORA_CLOTHING_BLACKLIST
                    or tag in LORA_POSE_BLACKLIST
                    or tag in LORA_MISC_BLACKLIST
                ):
                    print(f"tag: {tag}")
                    general_tags = general_tags.replace(tag, "")
                    print("removed clothing tag")

    except:
        print("no BLACKLIST category found")
        pass

    output_tags = character_tags + " " + general_tags

    output_tags_list = []
    output_tags_list = output_tags.split(", ")
    output_tags_list = list(filter(None, output_tags_list))
    output_tags_list = [x.strip() for x in output_tags_list]

    final_output_tags = ""
    for tag in output_tags_list:
        final_output_tags += tag + ", "

    if nai_option == True:
        final_output_tags = (
            "(masterpiece:1.2), (best quality:1.2), " + final_output_tags
        )

    return final_output_tags


def on_ui_settings():
    section = ("booru_tags", "Booru Tags")
    shared.opts.add_option(
        "booru_tags_danbooru_username",
        shared.OptionInfo("", "Danbooru Username", section=section),
    )
    shared.opts.add_option(
        "booru_tags_danbooru_apikey",
        shared.OptionInfo("", "Danbooru API key", section=section),
    )
    # shared.opts.add_option(
    #     "booru_tags_e621_username",
    #     shared.OptionInfo("", "e621 Username", section=section),
    # )
    # shared.opts.add_option(
    #     "booru_tags_e621_apikey",
    #     shared.OptionInfo("", "e621 API key", section=section),
    # )


def has_settings():
    if (
        hasattr(opts, "booru_tags_danbooru_username")
        and hasattr(opts, "booru_tags_danbooru_apikey")
        and len(opts.booru_tags_danbooru_username) > 0
        and len(opts.booru_tags_danbooru_apikey) > 0
    ):
        return True
    return False


class BooruPromptsScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

        self.is_useable = False

        if has_settings():
            # username = (opts.booru_prompts_danbooru_username,)
            # api_key = (opts.booru_prompts_danbooru_apikey,)
            pass
        else:
            # self.client: Danbooru = None # type: ignore
            pass

    def title(self):
        return "Booru Tags"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        (
            fetch_tags,
            output,
            search,
            lora_option,
            nai_option,
            booru_choice,
        ) = self._create_ui()

        return [
            fetch_tags,
            output,
            search,
            lora_option,
            nai_option,
            booru_choice,
        ]

    def _fetch(
        self,
        search: str,
        lora_option: bool,
        nai_option: bool,
        booru_choice: str,
        limit=1,
    ):
        try:
            dbusername = opts.booru_tags_danbooru_username
            dbapi_key = opts.booru_tags_danbooru_apikey
            # e621username_ = opts.booru_tags_e621_username
            # e621api_key_ = opts.booru_tags_e621_apikey

            set = getTags(
                search,
                lora_option,
                dbusername,
                dbapi_key,
                # e621username_,
                # e621api_key_,
                nai_option,
                booru_choice,
            )

            return set
        except:
            traceback.print_exc()
            return f"Error occurred, see console for more details."

    def _create_ui(self):
        self.is_useable = True

        with gr.Group():
            with gr.Accordion("Booru Tags", open=False):
                fetch_tags = gr.Button(
                    value="Search", variant="primary", visible=self.is_useable
                )

                with gr.Group(visible=self.is_useable):
                    with gr.Row():
                        output = gr.Textbox(label="Output", lines=4, interactive=False)
                        with gr.Column():
                            booru_choice = gr.Dropdown(
                                ["Danbooru", "Safebooru"],  # e621 removed for now
                                label="Booru Site",
                                value="Danbooru",
                                interactive=True,
                            )
                            parameters_copypaste.bind_buttons(
                                parameters_copypaste.create_buttons(
                                    ["txt2img", "img2img"],
                                ),
                                None,
                                output,
                            )

                    with gr.Row():
                        lora_option = gr.Checkbox(value=False, label="Using LoRA?")
                        nai_option = gr.Checkbox(value=False, label="Using NovelAI?")

                with gr.Group(visible=self.is_useable):
                    search = gr.Textbox(
                        placeholder="Post ID",
                        show_label=False,
                        value="https://danbooru.donmai.us/posts/5991704",
                    )

        fetch_tags.click(
            fn=lambda x1, x2, x3, x4: self._fetch(x1, x2, x3, x4),
            inputs=[search, lora_option, nai_option, booru_choice],
            outputs=[output],
            scroll_to_output=False,
            show_progress=True,
        )

        return output, search, lora_option, nai_option, booru_choice, fetch_tags


script_callbacks.on_ui_settings(on_ui_settings)
