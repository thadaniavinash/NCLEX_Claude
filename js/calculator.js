/* On-screen calculator. */

function initCalculator() {
  const btns = document.querySelectorAll('.calc-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const val = e.target.textContent.trim();
      const act = e.target.dataset.action;
      
      // Reset clear / mrc press counts if clicking a different action
      if (act !== 'clear') {
        clearPressCount = 0;
      }
      if (act !== 'mrc') {
        mrcPressCount = 0;
      }
      
      if (act === 'clear') {
        clearPressCount++;
        if (clearPressCount >= 2) {
          calcMemory = 0;
          clearPressCount = 0;
          showToast("Calculator memory cleared", "info");
        }
        calcInput = '0';
        calcPrevInput = null;
        calcOp = null;
        calcResetOnNext = false;
      } else if (act === 'sign') {
        if (calcInput !== '0' && calcInput !== 'Error') {
          calcInput = calcInput.startsWith('-') ? calcInput.slice(1) : '-' + calcInput;
        }
      } else if (act === 'sqrt') {
        let num = parseFloat(calcInput);
        if (num >= 0) {
          calcInput = Math.sqrt(num).toString().slice(0, 10);
        } else {
          calcInput = 'Error';
        }
        calcResetOnNext = true;
      } else if (act === 'percent') {
        let num = parseFloat(calcInput);
        calcInput = (num / 100).toString().slice(0, 10);
        calcResetOnNext = true;
      } else if (e.target.classList.contains('num-btn')) {
        if (calcInput === '0' || calcInput === 'Error' || calcResetOnNext) {
          calcInput = val;
          calcResetOnNext = false;
        } else {
          if (calcInput.length < 10) {
            if (val === '.' && calcInput.includes('.')) return;
            calcInput += val;
          }
        }
      } else if (e.target.classList.contains('op-btn')) {
        // Evaluate pending operation first (chaining support)
        if (calcPrevInput !== null && calcOp) {
          let curr = parseFloat(calcInput);
          let res = 0;
          switch (calcOp) {
            case 'add': res = calcPrevInput + curr; break;
            case 'subtract': res = calcPrevInput - curr; break;
            case 'multiply': res = calcPrevInput * curr; break;
            case 'divide': res = curr !== 0 ? calcPrevInput / curr : 'Error'; break;
          }
          calcInput = (res === 'Error') ? 'Error' : parseFloat(res.toFixed(8)).toString().slice(0, 10);
        }
        calcPrevInput = (calcInput === 'Error') ? null : parseFloat(calcInput);
        calcOp = act;
        calcResetOnNext = true;
      } else if (act === 'equals') {
        if (calcPrevInput !== null && calcOp) {
          let curr = parseFloat(calcInput);
          let res = 0;
          switch (calcOp) {
            case 'add': res = calcPrevInput + curr; break;
            case 'subtract': res = calcPrevInput - curr; break;
            case 'multiply': res = calcPrevInput * curr; break;
            case 'divide': res = curr !== 0 ? calcPrevInput / curr : 'Error'; break;
          }
          calcInput = (res === 'Error') ? 'Error' : parseFloat(res.toFixed(8)).toString().slice(0, 10);
          calcPrevInput = null;
          calcOp = null;
          calcResetOnNext = true;
        }
      } else if (e.target.classList.contains('mem-btn')) {
        if (act === 'mplus' || act === 'mminus') {
          // Evaluate pending operation first
          if (calcPrevInput !== null && calcOp) {
            let curr = parseFloat(calcInput);
            let res = 0;
            switch (calcOp) {
              case 'add': res = calcPrevInput + curr; break;
              case 'subtract': res = calcPrevInput - curr; break;
              case 'multiply': res = calcPrevInput * curr; break;
              case 'divide': res = curr !== 0 ? calcPrevInput / curr : 'Error'; break;
            }
            calcInput = (res === 'Error') ? 'Error' : parseFloat(res.toFixed(8)).toString().slice(0, 10);
            calcPrevInput = null;
            calcOp = null;
          }
          
          if (calcInput !== 'Error') {
            let num = parseFloat(calcInput);
            if (!isNaN(num)) {
              if (act === 'mplus') calcMemory += num;
              else if (act === 'mminus') calcMemory -= num;
            }
          }
          calcResetOnNext = true;
        } else if (act === 'mrc') {
          mrcPressCount++;
          if (mrcPressCount === 1) {
            calcInput = parseFloat(calcMemory.toFixed(8)).toString().slice(0, 10);
            calcResetOnNext = true;
          } else if (mrcPressCount >= 2) {
            calcMemory = 0;
            mrcPressCount = 0;
            showToast("Calculator memory cleared", "info");
          }
        }
      }
      
      updateCalculatorDisplay();
    });
  });

  document.addEventListener('keydown', (e) => {
    const calc = document.getElementById('ti108-calculator');
    if (!calc || calc.classList.contains('hidden')) return;

    // Ignore keypresses if focus is in an input or contenteditable element
    const activeEl = document.activeElement;
    if (activeEl && (
      activeEl.tagName === 'INPUT' || 
      activeEl.tagName === 'TEXTAREA' || 
      activeEl.contentEditable === 'true' || 
      activeEl.closest('[contenteditable="true"]')
    )) {
      return;
    }

    let btn = null;
    const key = e.key;

    if (key >= '0' && key <= '9') {
      btn = Array.from(calc.querySelectorAll('.num-btn')).find(b => b.textContent.trim() === key);
    } else if (key === '.') {
      btn = Array.from(calc.querySelectorAll('.num-btn')).find(b => b.textContent.trim() === '.');
    } else if (key === '+') {
      btn = calc.querySelector('[data-action="add"]');
    } else if (key === '-') {
      btn = calc.querySelector('[data-action="subtract"]');
    } else if (key === '*') {
      btn = calc.querySelector('[data-action="multiply"]');
    } else if (key === '/') {
      btn = calc.querySelector('[data-action="divide"]');
    } else if (key === '=' || key === 'Enter') {
      btn = calc.querySelector('[data-action="equals"]');
    } else if (key === 'Escape' || key === 'Backspace' || key.toLowerCase() === 'c') {
      btn = calc.querySelector('[data-action="clear"]');
    } else if (key === '%') {
      btn = calc.querySelector('[data-action="percent"]');
    } else if (key.toLowerCase() === 's') {
      btn = calc.querySelector('[data-action="sign"]');
    } else if (key.toLowerCase() === 'r') {
      btn = calc.querySelector('[data-action="sqrt"]');
    } else if (key.toLowerCase() === 'm') {
      btn = calc.querySelector('[data-action="mrc"]');
    } else if (key === '[') {
      btn = calc.querySelector('[data-action="mplus"]');
    } else if (key === ']') {
      btn = calc.querySelector('[data-action="mminus"]');
    }

    if (btn) {
      e.preventDefault();
      btn.click();
      btn.classList.add('active');
      setTimeout(() => btn.classList.remove('active'), 100);
    }
  });
}

function updateCalculatorDisplay() {
  const display = document.getElementById('calc-display');
  if (display) display.textContent = calcInput;
  
  const indicator = document.getElementById('calc-mem-indicator');
  if (indicator) {
    indicator.style.visibility = calcMemory !== 0 ? 'visible' : 'hidden';
  }
}

function toggleCalculator() {
  const calc = document.getElementById('ti108-calculator');
  if (calc.classList.contains('hidden')) {
    calc.classList.remove('hidden');
    calc.style.top = '50px';
    calc.style.left = '220px';
  } else {
    calc.classList.add('hidden');
  }
}

function makeCalculatorDraggable() {
  const calc = document.getElementById('ti108-calculator');
  const header = calc.querySelector('.calc-top-bar');
  
  if (!calc || !header) return;
  
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  
  header.addEventListener('mousedown', dragMouseDown);
  header.addEventListener('touchstart', dragTouchStart, { passive: false });
  
  function dragMouseDown(e) {
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.addEventListener('mouseup', closeDragElement);
    document.addEventListener('mousemove', elementDrag);
  }
  
  function dragTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    pos3 = touch.clientX;
    pos4 = touch.clientY;
    document.addEventListener('touchend', closeDragTouch);
    document.addEventListener('touchmove', elementTouchDrag, { passive: false });
  }
  
  function elementDrag(e) {
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    
    let finalTop = calc.offsetTop - pos2;
    let finalLeft = calc.offsetLeft - pos1;
    
    calc.style.top = Math.max(0, finalTop) + "px";
    calc.style.left = Math.max(0, finalLeft) + "px";
  }
  
  function elementTouchDrag(e) {
    e.preventDefault();
    const touch = e.touches[0];
    pos1 = pos3 - touch.clientX;
    pos2 = pos4 - touch.clientY;
    pos3 = touch.clientX;
    pos4 = touch.clientY;
    
    let finalTop = calc.offsetTop - pos2;
    let finalLeft = calc.offsetLeft - pos1;
    
    calc.style.top = Math.max(0, finalTop) + "px";
    calc.style.left = Math.max(0, finalLeft) + "px";
  }
  
  function closeDragElement() {
    document.removeEventListener('mouseup', closeDragElement);
    document.removeEventListener('mousemove', elementDrag);
  }
  
  function closeDragTouch() {
    document.removeEventListener('touchend', closeDragTouch);
    document.removeEventListener('touchmove', elementTouchDrag);
  }
}
