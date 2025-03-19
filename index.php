<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <title>Job Application Form</title>
</head>
<body>
    <div class="container mt-5">
        <h2 class="text-center">Job Application Form</h2>
        <form action="upload.php" method="POST" enctype="multipart/form-data">
            
            <!-- Full Name -->
            <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" class="form-control" name="name" id="name" required>
            </div>

            <!-- Email -->
            <div class="mb-3">
                <label for="email" class="form-label">Email Address</label>
                <input type="email" class="form-control" name="email" id="email" required>
            </div>

            <!-- Phone -->
            <div class="mb-3">
                <label for="phone" class="form-label">Phone Number</label>
                <input type="text" class="form-control" name="phone" id="phone" required>
            </div>

            <!-- Experience -->
            <div class="mb-3">
                <label for="experience" class="form-label">Work Experience</label>
                <textarea class="form-control" name="experience" id="experience" rows="3" required></textarea>
            </div>

            <!-- Skills -->
            <div class="mb-3">
                <label for="skills" class="form-label">Skills</label>
                <input type="text" class="form-control" name="skills" id="skills" required>
            </div>

            <!-- File Upload -->
            <div class="mb-3">
                <label for="file" class="form-label">Upload CV (PDF/DOC)</label>
                <input type="file" class="form-control" name="file" id="file" accept=".pdf,.doc,.docx" required>
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary w-100">Submit Application</button>
        </form>
    </div>
</body>
</html>
