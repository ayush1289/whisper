SEGMENTATION = "Segmentation model name from pyannote"
EMBEDDING = "Embedding model name from pyannote"
DURATION = "Chunk duration (in seconds)"
STEP = "Sliding window step (in seconds)"
LATENCY = "System latency (in seconds). STEP <= LATENCY <= CHUNK_DURATION"
TAU = "Probability threshold to consider a speaker as active. 0 <= TAU <= 1"
RHO = "Speech ratio threshold to decide if centroids are updated with a given speaker. 0 <= RHO <= 1"
DELTA = "Embedding-to-centroid distance threshold to flag a speaker as known or new. 0 <= DELTA <= 2"
GAMMA = "Parameter gamma for overlapped speech penalty"
BETA = "Parameter beta for overlapped speech penalty"
MAX_SPEAKERS = "Maximum number of speakers"
CPU = "Force models to run on CPU"
BATCH_SIZE = "For segmentation and embedding pre-calculation. If BATCH_SIZE < 2, run fully online and estimate real-time latency"
NUM_WORKERS = "Number of parallel workers"
OUTPUT = "Directory to store the system's output in RTTM format"
HF_TOKEN = "Huggingface authentication token for hosted models ('true' | 'false' | <token>). If 'true', it will use the token from huggingface-cli login"
SAMPLE_RATE = "Sample rate of the audio stream"
NORMALIZE_EMBEDDING_WEIGHTS = "Rescale embedding weights (min-max normalization) to be in the range [0, 1]. This is useful in some models without weighted statistics pooling that rely on masking, like Nvidia's NeMo or ECAPA-TDNN"
