import json
import os
import torch
import base64
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from typing import List
from huggingface_hub import InferenceClient
from cad_builder.utils import find_project_root


class PromptHandler:

    prompt_beginner =  """
        The following scenario:

        Given 6 images, each representing the same 3D object from different views. 
        The 3D object shown in the images is the result of a user prompt to a text to 3D SOTA model.
        The user's aim was to be able to use the 3D object in a CAD system.

        Prompt beginner:
        Let's assume the user does not have much experience with CAD.
        What could the user's prompt have looked like?
        The prompt should not be longer than 80 words.

        Only the prompt should be included in your answer. Do not use colour descriptions.
        Your answer must be in german.
        The format of your answer is as follows:

        prompt_beginner: <prompt>
    """

    prompt_intermediate =  """
        The following scenario:

        Given 6 images, each representing the same 3D object from different views.
        The 3D object shown in the images is the result of a user prompt to a text to 3D SOTA model.
        The user's aim was to be able to use the 3D object in a CAD system.

        Prompt intermediate:
        Assuming the user already has good experience with CAD.
        What could the user's prompt have looked like?
        The prompt should not be longer than 80 words.

        Only the prompt should be included in your answer. Do not use colour descriptions.
        Your answer must be in german.
        The format of your answer is as follows:

        prompt_intermediate: <prompt>
    """

    def __init__(self, model_name: str = "Qwen/Qwen2.5-VL-3B-Instruct", api_key="YOUR_API_KEY"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        ).to(self.device)
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.client = InferenceClient(api_key="api_key", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")

    def get_image_paths(self, image_folder: str) -> List[str]:
        return [
            os.path.join(image_folder, file_name)
            for file_name in sorted(os.listdir(image_folder))
            if file_name.lower().endswith(".png")
        ]

    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"
    
    def generate_prompts_local(self, image_folder: str) -> str:
        image_paths = self.get_image_paths(image_folder)
        vision_inputs = [{"type": "image", "image": f"file://{path}"} for path in image_paths]

        messages = [
            {"role": "user", "content": vision_inputs + [{"type": "text", "text": self.prompt_beginner}]},
            {"role": "user", "content": vision_inputs + [{"type": "text", "text": self.prompt_intermediate}]}
        ]
        print(messages)

        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=200)

        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, output)
        ]
        
        output_texts = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_texts[0], output_texts[1]


    def generate_prompts_api(self, image_folder: str, prompt_path: str) -> str:
        
        image_paths = self.get_image_paths(image_folder)
        vision_inputs = [{"type": "image_url", "image_url": {"url": self.encode_image(path)}} for path in image_paths]

        messages = [
            {"role": "user", "content": vision_inputs + [{"type": "text", "text": self.prompt_beginner}]},
            {"role": "user", "content": vision_inputs + [{"type": "text", "text": self.prompt_intermediate}]}
        ]

        responses = []

        for message in messages:
            output = self.client.chat.completions.create(messages=[message])
            responses.append(output['choices'][0]['message']['content'])


        prompt_beginner = responses[0].split("prompt_beginner: ")[1][1:-1]
        prompt_intermediate = responses[1].split("prompt_intermediate: ")[1][1:-1]

        prompt_json = {
            "prompt_beginner": prompt_beginner,
            "prompt_intermediate": prompt_intermediate
        }

        with open(f"{prompt_path}.json", "w") as json_file:
            json.dump(prompt_json, json_file, indent=4)


def create_prompts_for_all_stl_files(folder_path):
    stl_files = [f for f in os.listdir(folder_path) if f.endswith('.stl')]
    
    project_root = find_project_root(os.path.dirname("./"))
    prompt_handler = PromptHandler()

    for stl_file_name in stl_files:
        image_folder_path = os.path.join(project_root, f'cad_builder/data/images/{stl_file_name}')
        prompt_path = os.path.join(project_root, f'cad_builder/data/prompts/{stl_file_name}')
        prompt_handler.generate_prompts_api(image_folder=image_folder_path, prompt_path=prompt_path)

# Create prompts for all stl files and save in cad_builder/data/prompts
# create_prompts_for_all_stl_files()








