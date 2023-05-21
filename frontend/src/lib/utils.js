export const hexToRgb = hex =>
	hex.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i
		,(m, r, g, b) => '#' + r + r + g + g + b + b)
	.substring(1).match(/.{2}/g)
	.map(x => parseInt(x, 16));

export const rgbToHex = (r, g, b) => 
	'#' + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);

export const rgbToHsv = (r, g, b) => {
		let v=Math.max(r,g,b), c=v-Math.min(r,g,b);
	let h= c && ((v==r) ? (g-b)/c : ((v==g) ? 2+(b-r)/c : 4+(r-g)/c)); 
	return [60*(h<0?h+6:h), v&&c/v, v];
};

export const hsvToRgb = (h, s, v) => {
	let f= (n,k=(n+h/60)%6) => v - v*s*Math.max(Math.min(k,4-k,1), 0);
	return [f(5),f(3),f(1)];
};
