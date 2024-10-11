def run_bash_command(command):
	import subprocess
	try:
		command = f"cd /app && {command}"
		print("Command start:", command)
		result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
		print("Command executed successfully.")
		print("Result:", result.stdout)
		return result.stdout
	except subprocess.CalledProcessError as e:
		print("An error occurred while executing the command.")
		print("Return code:", e.returncode)
		print("Command output:", e.output)
		print("Command stderr:", e.stderr)
		return f"An error occurred: {e.stderr}"
