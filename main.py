from src.form_automation import run_automation
from utils.parse_args import parse_args
from utils.data_loader import excel_to_dict_list
import asyncio


if __name__ == "__main__":
    args = parse_args()
    data = excel_to_dict_list("data/challenge.xlsx")
    asyncio.run(run_automation(data, args))
