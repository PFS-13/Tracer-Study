import os
import shutil
import clyngor

from typing import Dict, List, Optional
from clyngor.answers import Answers
from visrec.src.Transform import Asp2Vl
import logging
import subprocess
import os
import tempfile
import json
from time import time
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_cache: Dict[str, bytes] = {}

DRACO_LP_DIR = './visrec/asps'
DRACO_LP = [
    "define.lp",
    "generate.lp",
    "rules.lp",
    "output.lp",
    "task.lp"
]

# Answer Class
class Result:
    props: List[str]
    cost: Optional[int]
    Ops: List[str]
    fields:List[str]
    count:int
    task:set()
    svg:List

    def __init__(self, answers: Answers, cost: Optional[int] = None):
        props: List[str] = []
        Ops: List[str] = []
        for ((head, body),) in answers:
            if head == "cost":
                cost = int(body[0])
            else:
                b = ",".join(map(str, body))
                props.append(f"{head}({b}).")

        self.props = props
        self.cost = cost
        self.Ops = []
        self.fields=[]
        self.count=0
        self.task=set()
        self.svg=[]

    def __lt__(self, other):  # override <操作符
        if self.count>other.count:
            return True
        elif self.count<other.count:
            return False
        elif self.cost < other.cost:
            return True
        return False
    
    def __eq__(self, other):
        return self.props == other.props

    def as_vl(self) -> Dict:
        return Asp2Vl(self.props)


def load_file(path: str):
    content = file_cache.get(path)
    if content is not None:
        return content
    with open(path,'r',encoding='UTF-8') as f:
        content = f.read().encode("utf8")
        file_cache[path] = content
        return content



#run_clingo() ini adalah wrapper untuk menjalankan solver ASP (Clingo) dari Python menggunakan subprocess. 
# Dia bertugas menggabungkan program ASP + file rule, lalu mengirimkannya ke Clingo, dan mengembalikan hasilnya.
def run_clingo(
        draco_query: List[str],
        constants: Dict[str, str] = None,
        files: List[str] = None,
        relax_hard=False,
        silence_warnings=False,
        debug=False):
    """Run CLingo and return stderr and stdout"""
    files = files or DRACO_LP

    if relax_hard and "hard-integrity.lp" in files:
        files.remove("hard-integrity.lp")

    constants = constants or {}

    options = ["--outf=2", "-n 0", "--project"]
    if silence_warnings:
        options.append("--warn=no-atom-undefined")
    for name, value in constants.items():
        options.append(f"-c {name}={value}")


    cmd = ["clingo"] + options
    logger.debug("Command: %s", " ".join(cmd))
    proc = subprocess.Popen(
        args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env={'PATH': os.environ['PATH']}
    )
    program = u"\n".join(draco_query)
    file_names = [os.path.join(DRACO_LP_DIR, f) for f in files]
    asp_program = b"\n".join(map(load_file, file_names)) + program.encode("utf8")
    # print("asp_program:", asp_program)
    if debug:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fd:
            fd.write(program)

            logger.info('Debug ASP with "clingo %s %s"',
                        " ".join(file_names), fd.name)
    stdout, stderr = proc.communicate(asp_program)
    # Example of unsatifisable stdout
    #     {
    #   "Solver": "clingo version 5.6.2",
    #   "Input": [
    #     "stdin"
    #   ],
    #   "Call": [
    #     {}
    #   ],
    #   "Result": "UNSATISFIABLE",
    #   "Models": {
    #     "Number": 0,
    #     "More": "no"
    #   },
    #   "Calls": 1,
    #   "Time": {
    #     "Total": 0.042,
    #     "Solve": 0.000,
    #     "Model": 0.000,
    #     "Unsat": 0.000,
    #     "CPU": 0.047
    #   }
    # }
    #
    #     {
    #   "Solver": "clingo version 5.6.2",
    #   "Input": [
    #     "stdin"
    #   ],
    #   "Call": [
    #     {
    #       "Witnesses": [
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e1,x)", "channel(5,y)", "bin(e1,10)", "aggregate(5,count)", "type(5,quantitative)", "mark(arc)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e1,x)", "channel(5,y)", "bin(e1,10)", "aggregate(5,count)", "type(5,quantitative)", "mark(bar)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e0,x)", "channel(5,y)", "bin(e0,10)", "aggregate(5,count)", "type(5,quantitative)", "mark(arc)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e0,x)", "channel(5,y)", "bin(e0,10)", "aggregate(5,count)", "type(5,quantitative)", "mark(bar)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e0,y)", "channel(e1,x)", "bin(e1,10)", "aggregate(e0,sum)", "mark(bar)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e0,y)", "channel(e1,x)", "bin(e1,10)", "aggregate(e0,mean)", "mark(bar)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e0,x)", "channel(e1,y)", "bin(e0,10)", "aggregate(e1,sum)", "mark(bar)"]
    #         },
    #         {
    #           "Value": ["data(\"./values\")", "field(e0,\"Happiness Rank\")", "field(e1,\"Happiness Score\")", "type(e0,quantitative)", "type(e1,quantitative)", "channel(e0,x)", "channel(e1,y)", "bin(e0,10)", "aggregate(e1,mean)", "mark(bar)"]
    #         }
    #       ]
    #     }
    #   ],
    #   "Result": "SATISFIABLE",
    #   "Models": {
    #     "Number": 8,
    #     "More": "no"
    #   },
    #   "Calls": 1,
    #   "Time": {
    #     "Total": 0.044,
    #     "Solve": 0.003,
    #     "Model": 0.001,
    #     "Unsat": 0.001,
    #     "CPU": 0.047
    #   }
    # }
    return (stderr, stdout)


lock = threading.Lock()

# Mengirim query ASP ke Clingo
# Mengambil hasilnya
# Mengubah hasil jadi objek Python
def run(
        draco_query: List[str],
        constants: Dict[str, str] = None,
        files: List[str] = None,
        relax_hard=False,
        silence_warnings=False,
        debug=False,
        clear_cache=False,
        num=10):
    """ Run clingo to compute a completion of a partial spec or violations. """
    # Clear file cache. useful during development in notebooks.
    if clear_cache and file_cache:
        logger.warning("Cleared file cache")
        file_cache.clear()
    
    #example of draco_query
    # ['data("./values").', 'encoding(e0).', 'field(e0,"Happiness Rank").', 'type(e0,quantitative).',
    #  'encoding(e1).', 'field(e1,"Happiness Score").', 'type(e1,quantitative).', 'task(compute_derived_value).', 
    #  'num_rows(315).', 'fieldtype("Happiness Rank",number).', 'cardinality("Happiness Rank",158).', 'fieldtype("Happiness Score",number).', 'cardinality("Happiness Score",299).']
    
    # Call CLingo
    # time_s = time()
    stderr, stdout = run_clingo(
        draco_query, constants, files, relax_hard, silence_warnings, debug
    )
    # stdout → hasil utama (format JSON)
    # stderr → error/log

    # time_e = time()
    # print("Clingo time last %f " % (time_e - time_s))
    try:
        json_result = json.loads(stdout)
    except json.JSONDecodeError:
        logger.error("stdout: %s", stdout)
        logger.error("stderr: %s", stderr)
        raise
    # Analysis CLingo stdout

    result = json_result["Result"]
    #example of result : Satsifiable / unsatisfiable
    if result == "OPTIMUM FOUND" or result == "SATISFIABLE":
        StdoutNumber = json_result["Models"]["Number"]
        if num == 0:
            AnsNumber = StdoutNumber
        else:
            AnsNumber = StdoutNumber if StdoutNumber < num else num
        if "Witnesses" in json_result["Call"][0]:
            answers = json_result["Call"][0]["Witnesses"][StdoutNumber - AnsNumber:]
            answers.reverse()
        else:
            return None
        AnswerList=[]
        for i in range(AnsNumber):
        #     # if 'Cost' in answers[i]:
        #     #     AnswerList.append(Result(clyngor.Answers(answers[i]["Value"]).sorted, cost=answers[i]["Costs"]))
        #     # else:
            AnswerList.append(Result(clyngor.Answers(answers[i]["Value"]).sorted, cost=0))
        return AnswerList
    else:
        logger.error("Unsupported result: %s", result)
        return None
