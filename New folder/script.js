const STORAGE_KEY = 'STUDENT_LIST_APP';

function getStudents() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
}

function saveStudents(students) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(students));
}

function setInvalid(id, message) {
    const input = document.getElementById(id);
    if (!input) return;
    input.classList.add('is-invalid');
    const feedback = input.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.innerText = message;
    }
}

// --- XỬ LÝ TRANG ĐĂNG KÝ (register-student.html) ---
const studentForm = document.getElementById('studentForm');
if (studentForm) {
    const urlParams = new URLSearchParams(window.location.search);
    const editId = urlParams.get('editId');

    if (editId) {
        document.getElementById('formTitle').innerText = "Chỉnh sửa Sinh viên";
        const students = getStudents();
        const student = students.find(s => s.studentId === editId);
        
        if (student) {
            document.getElementById('fullName').value = student.fullName;
            document.getElementById('studentId').value = student.studentId;
            document.getElementById('studentId').disabled = true;
            document.getElementById('email').value = student.email;
            document.getElementById('phone').value = student.phone;
            document.getElementById('major').value = student.major;
            document.querySelector(`input[name="gender"][value="${student.gender}"]`).checked = true;
        }
    }

    studentForm.onsubmit = function(e) {
        e.preventDefault();
        const inputs = document.querySelectorAll('.form-control, .form-select');
        inputs.forEach(i => i.classList.remove('is-invalid'));

        const studentData = {
            fullName: document.getElementById('fullName').value.trim(),
            studentId: document.getElementById('studentId').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            major: document.getElementById('major').value,
            gender: document.querySelector('input[name="gender"]:checked').value
        };

        let isValid = true;
        if (studentData.fullName.length < 2) { setInvalid('fullName', 'Tên quá ngắn'); isValid = false; }
        if (!/^SV\d+$/.test(studentData.studentId)) { setInvalid('studentId', 'Mã SV sai định dạng'); isValid = false; }
        if (!studentData.email.includes('@')) { setInvalid('email', 'Email sai'); isValid = false; }

        if (isValid) {
            let students = getStudents();
            if (editId) {
                students = students.map(s => s.studentId === editId ? studentData : s);
                alert("Cập nhật thành công!");
            } else {
                if (students.some(s => s.studentId === studentData.studentId)) {
                    setInvalid('studentId', 'Mã sinh viên này đã tồn tại!');
                    return;
                }
                students.push(studentData);
                alert("Thêm mới thành công!");
            }
            saveStudents(students);
            window.location.href = 'students.html';
        }
    };
}

// --- XỬ LÝ TRANG DANH SÁCH (students.html) ---
const tableBody = document.getElementById('studentTableBody');
const filterMajor = document.getElementById('filterMajor');

if (tableBody) {
    function renderTable(filterValue = 'all') {
        const students = getStudents();
        tableBody.innerHTML = '';
        const emptyMsg = document.getElementById('emptyMessage');

        // Logic lọc dữ liệu
        const filteredStudents = filterValue === 'all' 
            ? students 
            : students.filter(s => s.major === filterValue);

        if (filteredStudents.length === 0) {
            emptyMsg.classList.remove('hidden');
            return;
        }

        emptyMsg.classList.add('hidden');
        filteredStudents.forEach(s => {
            tableBody.innerHTML += `
                <tr>
                    <td>${s.fullName}</td>
                    <td>${s.studentId}</td>
                    <td>${s.email}</td>
                    <td>${s.phone}</td>
                    <td>${s.major}</td>
                    <td>${s.gender}</td>
                    <td class="text-end">
                        <a href="register-student.html?editId=${s.studentId}" class="btn btn-sm btn-outline-primary">Sửa</a>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteStudent('${s.studentId}')">Xóa</button>
                    </td>
                </tr>`;
        });
    }

    // Sự kiện khi thay đổi bộ lọc
    if (filterMajor) {
        filterMajor.addEventListener('change', (e) => {
            renderTable(e.target.value);
        });
    }

    window.deleteStudent = function(id) {
        if (confirm("Xóa sinh viên này?")) {
            const students = getStudents().filter(s => s.studentId !== id);
            saveStudents(students);
            // Re-render với giá trị filter hiện tại
            renderTable(filterMajor ? filterMajor.value : 'all');
        }
    };

    renderTable();
}