from enum import Enum
import os
import logging
import time

class JobState(Enum):
    CREATED = "CREATED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SUCCEED = "SUCCEED"

class Job:
    def __init__(self, src, asm, output, model, log=None, timeout=1000, max_iter=10):
        # Validate parameters
        if not (os.path.isfile(src) and src.endswith(('.c', '.cpp'))):
            raise ValueError("Invalid source file path or format.")
        if not asm.endswith('.s'):
            raise ValueError("Assembly file must have a '.s' extension.")
        if timeout <= 0:
            raise ValueError("Timeout must be a positive integer.")
        if max_iter <= 0:
            raise ValueError("Maximum iterations must be a positive integer.")

        # Initialize attributes
        self.src = src
        self.asm = asm
        self.output = output
        self.model = model
        self.log = log
        self.timeout = timeout
        self.max_iter = max_iter
        self.state = JobState.CREATED

        # Setup logging if log path is provided
        if log:
            logging.basicConfig(filename=log, level=logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)

    def __call__(self):
        return self.run()

    def run(self):
        logging.info("Job started.")
        self.state = JobState.RUNNING
        start_time = time.time()

        try:
            # Parse assembly instructions
            instructions = self.parse()

            # Annotate the assembly file
            annotated_output = self.annotate(instructions)

            # Save output
            with open(self.output, 'w') as f:
                f.write(annotated_output)

            self.state = JobState.SUCCEED
            logging.info("Job completed successfully.")
        except Exception as e:
            self.state = JobState.FAILED
            logging.error(f"Job failed with error: {e}")
        finally:
            elapsed_time = (time.time() - start_time) * 1000  # ms
            if elapsed_time > self.timeout:
                self.state = JobState.FAILED
                logging.error("Job exceeded the timeout.")

        return self.state

    def parse(self):
        """Parses the assembly file to extract instructions."""
        if not os.path.isfile(self.asm):
            raise FileNotFoundError(f"Assembly file '{self.asm}' not found.")

        with open(self.asm, 'r') as file:
            lines = file.readlines()

        instructions = [line.strip() for line in lines if line.strip() and not line.startswith(";")]
        logging.info(f"Parsed {len(instructions)} instructions from the assembly file.")
        return instructions

    def annotate(self, instructions):
        """Annotates the assembly instructions using the model."""
        annotated = []
        for i, instruction in enumerate(instructions):
            # Simulate annotation (replace with actual model logic)
            comment = f"; Annotation for instruction {i+1}"
            annotated.append(f"{instruction} {comment}")

        logging.info("Annotation completed.")
        return "\n".join(annotated)
