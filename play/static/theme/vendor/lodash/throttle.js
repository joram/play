var debounce=require("./debounce"),isObject=require("./isObject"),FUNC_ERROR_TEXT="Expected a function";function throttle(e,i,t){var n=!0,r=!0;if("function"!=typeof e)throw new TypeError(FUNC_ERROR_TEXT);return isObject(t)&&(n="leading"in t?!!t.leading:n,r="trailing"in t?!!t.trailing:r),debounce(e,i,{leading:n,maxWait:i,trailing:r})}module.exports=throttle;