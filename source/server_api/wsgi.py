from main import api
from predict.normalize_text import normalize_text
import runpy


if __name__ == "__main__":
    runpy._run_module_as_main("normalize_text")

    api.run()