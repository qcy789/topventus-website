// ===== 移动端菜单 =====
document.addEventListener('DOMContentLoaded', function() {
  var mobileToggle = document.getElementById('mobileToggle');
  var nav = document.getElementById('nav');
  if (mobileToggle && nav) {
    mobileToggle.addEventListener('click', function() {
      nav.classList.toggle('open');
    });
    document.querySelectorAll('#nav a').forEach(function(link) {
      link.addEventListener('click', function() {
        nav.classList.remove('open');
      });
    });
  }

  // ===== 表单提交 =====
  var inquiryForm = document.getElementById('inquiryForm');
  if (inquiryForm) {
    inquiryForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var modal = document.getElementById('successModal');
      if (modal) modal.classList.add('show');
      inquiryForm.reset();
    });
  }

  // ===== 滚动动画 =====
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-up, .stagger').forEach(function(el) {
    observer.observe(el);
  });
});

// ===== 返回顶部按钮 =====
window.addEventListener('scroll', function() {
  var btn = document.getElementById('backToTop');
  if (btn) {
    if (window.pageYOffset > 300) {
      btn.style.display = 'flex';
    } else {
      btn.style.display = 'none';
    }
  }
});
