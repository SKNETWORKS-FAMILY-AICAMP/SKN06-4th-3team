// account/static/account/js/check.js

// 가입/정보수정시 이름 글자수 체크
// submit 이벤트 처리 handler
function check_name_length(name) {
    if (name.length < 2) {
        alert('이름은 2글자 이상 입력하세요.');
        return false;
    }
}