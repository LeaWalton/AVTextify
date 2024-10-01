using System;
using System.Diagnostics;
using System.IO;

namespace AVTextify.CSharp {
    class Program {
        static void Main(string[] args) {
            Console.WriteLine("Welcome to AVTextify!");

            // Ask the user for the MP4 file path
            Console.WriteLine("Starting transcription process...");
            string mp4File = @"C:\Users\Leawa\Desktop\20240926_203401.mp4";

            // Set the output CSV path (same directory as the MP4)
            string outputCsv = Path.ChangeExtension(mp4File, ".csv");

            // Path to the Python script and Python executable
            string pythonPath = @"C:\Users\Leawa\AppData\Local\Programs\Python\Python312\python.exe";
            string scriptPath = @"E:\CodeProjects\AVTextify\src\AVTextify.Python\transcribe.py"; // Adjust as needed

            ProcessStartInfo start = new ProcessStartInfo {
                FileName = pythonPath,
                Arguments = $"\"{scriptPath}\" \"{mp4File}\" \"{outputCsv}\"",
                UseShellExecute = false,  // Important for capturing output
                RedirectStandardOutput = true,  // Capture standard output
                RedirectStandardError = true,   // Capture error output
                CreateNoWindow = true           // Run without creating a new window
            };

            try {
                Console.WriteLine("Launching Python process...");
                using (Process process = Process.Start(start)) {
                    if (process == null) {
                        Console.WriteLine("Failed to start the Python process.");
                        return;
                    }

                    Console.WriteLine("Python process started, capturing output...");

                    // Read standard output and error line by line
                    using (StreamReader reader = process.StandardOutput)
                    using (StreamReader errorReader = process.StandardError) {
                        string line;
                        while ((line = reader.ReadLine()) != null) {
                            Console.WriteLine($"Output: {line}");  // Print each line of the output
                        }

                        string errors;
                        while ((errors = errorReader.ReadLine()) != null) {
                            Console.WriteLine($"Error: {errors}");  // Print each line of the error output
                        }
                    }

                    process.WaitForExit();  // Wait for the process to exit

                    Console.WriteLine($"Process exited with code: {process.ExitCode}");

                    if (process.ExitCode != 0) {
                        Console.WriteLine("There was an issue with the transcription process.");
                    }
                    else {
                        Console.WriteLine("Transcription completed. CSV saved to: " + outputCsv);
                    }
                }
            }
            catch (Exception ex) {
                Console.WriteLine($"Error running transcription: {ex.Message}");
            }
        }
    }
}
