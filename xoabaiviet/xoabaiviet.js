setInterval(() => {

    window.scrollBy(0, 100);
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    }
    const divContainer = document.querySelectorAll('div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd');
    const divbaishare = document.querySelectorAll('div.xdj266r.xat24cr.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1jx94hy.x8cjs6t.x1ch86jh.x80vd3b.xckqwgs.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x178xt8z.xm81vs4.xso031l.xy80clv.xfh8nwu.xoqspk4.x12v9rci.x138vmkv.x6ikm8r.x10wlt62.x16n37ib.xq8finb');
    const nut3cham = document.querySelectorAll('div[aria-label="Hành động với bài viết này"]');
    const reels = document.querySelectorAll('a[aria-label="Mở thước phim trong Công cụ xem của Reels"]');

    for (let element of divContainer) {
        const containsDivBaiShare = Array.from(divbaishare).some(child => element.contains(child));
        const containsNut3Cham = Array.from(nut3cham).some(child => element.contains(child));
        var contraireels = Array.from(reels).some(child => element.contains(child));
        if (containsDivBaiShare && containsNut3Cham || contraireels) {
            const button3Cham = element.querySelector('div[aria-label="Hành động với bài viết này"]');
            if (button3Cham) {
                console.log("click element !");
                button3Cham.click();
                break;
            }
        }
    }
    setTimeout(() => {
        const elements = document.querySelectorAll('div.x1ey2m1c.xds687c.x17qophe.xg01cxk.x47corl.x10l6tqk.x13vifvy.x1ebt8du.x19991ni.x1dhq9h.x9jk4nr.x10vv0rk.x1mn05ot.x4u6ece');
        console.log("số element :", elements.length);
        if (elements.length > 0) {
            const lastElement = elements[elements.length - 1];
            lastElement.click();
        } else {
            console.log("Không tìm thấy phần tử");
        }
    }, 2000);
    setTimeout(() => {
        console.log("done");
        const elements = document.querySelector('div[aria-label="Chuyển"]');
        const elements1 = document.querySelector('div[aria-label="Xóa"]');
        
        if (elements) {
            elements.click();
        }else if (elements1) {
            elements1.click();
        }
         else {
            console.log("không thấy nút chuyển'Chuyển'");
        }
    }, 2000);
}, 1000);