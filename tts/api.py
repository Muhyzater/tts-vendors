import traceback
import warnings
from io import BytesIO

from flask import Response, g, render_template, request, send_file
from micro_service import MicroService, Param, ParamSources, get_blueprint

from audio_configs import audio_params
from factory import TtsFactory
from tts.cache import Cache

warnings.filterwarnings("ignore")

blueprint = get_blueprint()


def tts_vendors_service(run=False, **kwargs):
    global g_tts
    global m_tts
    global salma_tts
    global text_cache
    params = audio_params
    params.update(kwargs)

    tts_vendors = MicroService(__name__, **params)
    cfg = tts_vendors.config

    text_cache = Cache(cfg["redis_host"], cfg["redis_port"], cfg["redis_db"])
    g_tts = TtsFactory.get_tts_obj(
        "google", cfg["google_config"], cfg["google_voice"], text_cache)
    m_tts = TtsFactory.get_tts_obj(
        "microsoft", cfg["microsoft_config"], cfg["microsoft_voice"], text_cache
    )
    salma_tts = TtsFactory.get_tts_obj(
        "salmaai", cfg["salma_config"], None, text_cache)
    tts_vendors.register_blueprint(blueprint)
    if run:
        tts_vendors.run_service()
    else:
        return tts_vendors


@blueprint.route(
    "/tts",
    methods=["POST", "GET"],
    params=[
        Param(
            name="text",
            type=str,
            required=True,
            source=[ParamSources.ARGS, ParamSources.BODY_FORM,
                    ParamSources.BODY_JSON],
        ),
        Param(
            name="vendor",
            type=str,
            required=False,
            default=audio_params["vendor"],
            source=[ParamSources.ARGS, ParamSources.BODY_FORM,
                    ParamSources.BODY_JSON],
            possible_values=["google", "microsoft", "salmaai"],
        ),
        Param(
            name="encoding",
            type=str,
            required=False,
            default=audio_params["encoding"],
            source=[ParamSources.ARGS, ParamSources.BODY_FORM,
                    ParamSources.BODY_JSON],
        ),
        Param(
            name="rate",
            type=int,
            required=False,
            default=22050,
            source=[ParamSources.ARGS, ParamSources.BODY_FORM,
                    ParamSources.BODY_JSON],
            min=16000,
            max=48000,
        ),
        Param(
            name="tashkeel",
            type=bool,
            required=False,
            default=audio_params["tashkeel"],
            source=[ParamSources.ARGS, ParamSources.BODY_FORM,
                    ParamSources.BODY_JSON],
        ),
    ],
)
def vendor_tts_endpoint():
    cfg = g.config
    p = g.params
    key = "{}#{}".format(p["vendor"], p["text"])

    try:

        if p["vendor"] == "google":
            output = g_tts.text_to_audio(
                p["encoding"],
                p["rate"],
                p["text"],
                key,
                p["tashkeel"]
            )
        elif p["vendor"] == "microsoft":
            output = m_tts.text_to_audio(
                p["encoding"], p["rate"], p["text"], key, p["tashkeel"]
            )
        elif p["vendor"] == "salmaai":
            output = salma_tts.text_to_audio(
                p["encoding"], p["rate"], p["text"], key, p["tashkeel"]
            )

        _file_name = "output_audio.{}".format(p["encoding"])
        _audio = send_file(
            BytesIO(output),
            mimetype="audio/" + p["encoding"],
            as_attachment=True,
            attachment_filename=_file_name,
        )

        if isinstance(output, Exception):
            raise Exception(str(output))

        return _audio, 200, cfg["headers"]

    except Exception as ex:
        traceback.print_exc()
        response = "FAIL"
        return response, 500, cfg["headers"]


@blueprint.route("/demo", methods=["GET"])
def demo_page():
    samples = [
        "بِالنِسْبِة لَلتَأْمِيناتْ أنا  مُمْكِنْ أَوَفِّرْلَكِ المَعْلُوماتِ التالِيِة عَنْ أَنْواعِ التَأْمِيناتْ إِلِّي بِقَدِّمْها البَنْكْ.",
        "بَرْنامَجْ رُويال وُبَرْنامَجِ العُونْ لَتَأْمِينْ مِتْكامِلْ لَلعِلاجاتِ السِنِّيِّة بْجَمِيعْ أَنْواعْها.",
        "مَرْكَزِ الاِتِّصالِ المُباشِرْ بِخِدْمِتَكْ عَلَى مَدارْ أَرْبَعَة وُعِشْرِينْ ساعَة.",
        "كِيفَك يَا زَلَمِه.",
        "مَرحَبا, مَعْكُمْ نورا مِن شِركِةْ مَوضوعْ, وُ أَهلاْ و سَهْلاْ فِيكُمْ بِالإِجْتِماعْ.",
        "لماذا تقوم بهذا العمل؟",
    ]
    return Response(
        render_template("demo.html", samples=samples,
                        root_path=g.config["root_path"])
    )


app = tts_vendors_service()


def run():
    app.run_service()


if __name__ == "__main__":
    run()
