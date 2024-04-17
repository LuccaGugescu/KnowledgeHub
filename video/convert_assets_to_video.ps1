# Get the directory of the current script
$scriptDirectory = $PSScriptRoot

# Specify the input files relative to the script directory
$imagePattern = Join-Path -Path $scriptDirectory -ChildPath "image%d.png"
$audioFile = Join-Path -Path $scriptDirectory -ChildPath "audio.mp3"
$outputFile = Join-Path -Path $scriptDirectory -ChildPath "converted_video.mp4"

# Run FFmpeg command
ffmpeg -y `
-framerate 1/5 `
-i $imagePattern `
-i $audioFile `
-vf "fps=24" `
-c:v libx264 `
-pix_fmt yuv420p `
-c:a aac `
-strict experimental `
$outputFile
