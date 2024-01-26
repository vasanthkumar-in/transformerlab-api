# This plugin exports a model to GGUF format so you can interact and train on a MBP with Apple Silicon
import os
import subprocess
import sqlite3
import argparse
import sys
import json
import time

# Get all arguments provided to this script using argparse
parser = argparse.ArgumentParser(description='Convert a model to GGUF format.')
parser.add_argument('--model_name', default='gpt-j-6b', type=str, help='Name of model to export.')
parser.add_argument('--model_architecture', default='hf-causal', type=str, help='Type of model to export.')
parser.add_argument('--experiment_name', default='', type=str, help='Name of experiment.')
parser.add_argument('--quant_bits', default='4', type=str, help='Bits per weight for quantization.')
args, unknown = parser.parse_known_args()

# TODO: Verify that the model uses a supported format (see main.json for list)
model_architecture = args.model_architecture

# Directory to run conversion subprocess
root_dir = os.environ.get("LLM_LAB_ROOT_PATH")
plugin_dir = f"{root_dir}/workspace/experiments/{args.experiment_name}/plugins/gguf_exporter"

# Use the original model's ID to name the converted model
model_id = args.model_name.split("/")[-1]
conversion_time = int(time.time())
output_model_name = f"gguf-{model_id}-{conversion_time}"

# Name of directory to output quantized model
# Generate a name with a timestamp and create the directory
output_dir = f"{root_dir}/workspace/models/{output_model_name}"
os.makedirs(output_dir)

# Call GGUF Convert function
# TODO: This is a placeholder for now! Sleep 10 seconds to test app functionality
print("Exporting", args.model_name, "to GGUF format in", output_dir)
export_process = subprocess.run(
#    ["python", '-u', '-m',  _TODO_conversion_class, '--hf-path', args.model_name, '--output-path', output_dir, '-q', '--q-bits', str(args.quant_bits)],
    ["sleep", 10],
    cwd=plugin_dir,
    capture_output=True
)

# If model create was successful, create an info.json file so this can be read by the system
if (export_process.returncode == 0):
    model_description = [{
        "model_id": f"TransformerLab-gguf/{output_model_name}",
        "model_filename": output_model_name,
        "name" : f"{model_id} - GGUF {args.quant_bits}bit",
        "local_model": True,
        "json_data" : {
            "uniqueID": f"TransformerLab-gguf/{output_model_name}",
            "name": output_model_name,
            "description": f"A GGUF model generated by TransformerLab based on {args.model_name}",
            "architecture": "GGUF",
            "quantization_bits": str(args.quant_bits),
            "huggingface_repo": ""
        }
    }]
    model_description_file = open(f"{output_dir}/info.json", "w")
    json.dump(model_description, model_description_file)
    model_description_file.close()

    print("Export to GGUF completed successfully")

else:
    print("Export to GGUF failed. Return code:", export_process.returncode)
