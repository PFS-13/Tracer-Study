import json
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

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


@router.post("/Reco")
def recommendation(request: RecommendationRequest):

    dataset = request.dataset
    column_types = request.ColumnTypes
    task = request.task
    mode = request.mode
    print("==request :==",request)
    BASE_DIR = Path(__file__).resolve().parent
    url = BASE_DIR.parent / "dataset" / f"{dataset}.json"
    with open(url, 'r', encoding='UTF-8') as f:
        data_json = json.load(f)
    
    recos, data = TaskVisAPIs(
        Data=data_json,
        ColumnTypes=column_types,
        task=task,
        Num=0,
        mode=1
    )

    result = {
        "Data": data,
        "Recos": recos
    }

    return result

