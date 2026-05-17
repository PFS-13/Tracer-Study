import json
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
import math
from visrec.src.main import TaskVisAPIs

router = APIRouter(
    prefix="/api",
    tags=["Dataset"]
)


class RecommendationRequest(BaseModel):
    dataset: str
    ColumnTypes: list
    task: list
    mode: int


@router.get("/columns")
def get_columns(dataset: str):

    columns = None

    if dataset == "mahasiswa":
        columns = [
            {"field": "nama", "type": "nominal"},
            {"field": "nim", "type": "nominal"},
            {"field": "jenis_kelamin", "type": "nominal"},
            {"field": "angkatan", "type": "temporal"},
            {"field": "program_studi", "type": "nominal"},
            {"field": "ipk", "type": "quantitative"},
            {"field": "tahun_lulus", "type": "temporal"},
            {"field": "penawaran_kontrak_sebelum_lulus", "type": "nominal"},
            {"field": "bekerja_saat_kuliah", "type": "nominal"},
            {"field": "wiraswasta_saat_kuliah", "type": "nominal"},
            {"field": "mulai_mencari_pekerjaan_bulan", "type": "quantitative"},
            {"field": "mulai_mencari_pekerjaan_sebelum_lulus_bulan", "type": "quantitative"},
            {"field": "mulai_mencari_pekerjaan_setelah_lulus_bulan", "type": "quantitative"},
            {"field": "pendapatan_per_bulan", "type": "quantitative"},
            {"field": "lokasi_kerja", "type": "nominal"},
            {"field": "jenis_perusahaan", "type": "nominal"},
        ]

    return columns


def find_invalid(obj, path="root"):

    # DICT
    if isinstance(obj, dict):

        for k, v in obj.items():

            find_invalid(
                v,
                f"{path}.{k}"
            )

    # LIST
    elif isinstance(obj, list):

        for i, v in enumerate(obj):

            find_invalid(
                v,
                f"{path}[{i}]"
            )

    # FLOAT
    elif isinstance(obj, float):

        if math.isnan(obj):

            print(
                f"[NAN FOUND] {path}"
            )

        if math.isinf(obj):

            print(
                f"[INF FOUND] {path}"
            )

@router.post("/Reco")
def recommendation(request: RecommendationRequest):

    print("\n========================")
    print("REQUEST MASUK")
    print("========================")

    dataset = request.dataset
    column_types = request.ColumnTypes
    task = request.task
    mode = request.mode

    print("dataset :", dataset)
    print("column_types :", column_types)
    print("task :", task)
    print("mode :", mode)

    BASE_DIR = Path(__file__).resolve().parent

    url = (
        BASE_DIR.parent /
        "dataset" /
        f"{dataset}.json"
    )

    print("\nPATH DATASET:")
    print(url)

    with open(
        url,
        'r',
        encoding='UTF-8'
    ) as f:

        data_json = json.load(f)

    print("\nDATASET BERHASIL LOAD")

    print("\nMENJALANKAN TaskVisAPIs()")

    recos, data = TaskVisAPIs(
        Data=data_json,
        ColumnTypes=column_types,
        task=task,
        Num=0,
        mode=mode
    )
    result = {
        "Data": data,
        "Recos": recos
    }

    # print("\nCEK result")
    # find_invalid(result, "result")

    # print("\nSEBELUM RETURN")

    return result
