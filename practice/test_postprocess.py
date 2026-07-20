from backend.inference.postprocess import PostProcessor

processor = PostProcessor()

probabilities = [
    0.04156486,
    0.13505061,
    0.81134135,
    0.01204318
]

result = processor.process(probabilities)

print(result)