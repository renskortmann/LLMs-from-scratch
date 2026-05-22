import torch

inputs = torch.tensor(
  [[0.43, 0.15, 0.89], # Your     (x^1)
   [0.55, 0.87, 0.66], # journey  (x^2)
   [0.57, 0.85, 0.64], # starts   (x^3)
   [0.22, 0.58, 0.33], # with     (x^4)
   [0.77, 0.25, 0.10], # one      (x^5)
   [0.05, 0.80, 0.55]] # step     (x^6)
)

# attn_scores_for_loops = torch.empty(6, 6)

# for i, x_i in enumerate(inputs):
#    for j, x_j in enumerate(inputs):
#         attn_scores_for_loops[i, j] = torch.dot(x_i, x_j)

# print(attn_scores_for_loops)

attn_scores = inputs @ inputs.T
#print(attn_scores)

attn_weights = torch.softmax(attn_scores, dim=-1)
#print(attn_weights)
#print("All row sums: ", attn_weights.sum(dim=-1))

context_vecs = attn_weights @ inputs
print(context_vecs)