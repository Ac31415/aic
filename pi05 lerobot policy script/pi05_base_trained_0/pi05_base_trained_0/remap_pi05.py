import torch
from safetensors.torch import load_file, save_file
from pathlib import Path

# Adjust this to the actual snapshot path on your system
policy_path = Path("/home/minghanwei/.cache/huggingface/hub/models--caai-aic--trained_models_pi05_base_sfp_to_sfp_port_0_of_nic_card_mount_0_sc_to_sc_port_base_of_sc_port_0_4/snapshots/7189adef7f1a7d22ed2ba1c778b4b81127f93eca")

# 1. Load the original openpi weights
print("Reading original weights...")
state_dict = load_file(policy_path / "model.safetensors")

# 2. Fix keys to lerobot format (mimicking what `_fix_pytorch_state_dict_keys` does)
remapped = {}
for k, v in state_dict.items():
    if "gemma_expert.model" in k and ("input_layernorm" in k or "post_attention_layernorm" in k or "norm.weight" in k):
        continue
        
    new_k = k.replace("action_time_mlp_in", "time_mlp_in").replace("action_time_mlp_out", "time_mlp_out")
    
    if new_k in ["model.paligemma_with_expert.paligemma.lm_head.weight", "paligemma_with_expert.paligemma.lm_head.weight"]:
        new_k = "model.paligemma_with_expert.paligemma.model.language_model.embed_tokens.weight"
        
    if not new_k.startswith("model."):
        new_k = f"model.{new_k}"
        
    if "state_proj" not in new_k:
        remapped[new_k] = v
        
# 3. Save the clean "lerobot native" weights
print("Saving native weights...")
save_file(remapped, policy_path / "model_native.safetensors")
print("Done!")