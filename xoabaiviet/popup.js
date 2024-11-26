setInterval(() => {
    const divContainer = document.querySelectorAll('div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd');
    const divbaishare = document.querySelectorAll('div.xdj266r.xat24cr.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1jx94hy.x8cjs6t.x1ch86jh.x80vd3b.xckqwgs.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x178xt8z.xm81vs4.xso031l.xy80clv.xfh8nwu.xoqspk4.x12v9rci.x138vmkv.x6ikm8r.x10wlt62.x16n37ib.xq8finb');
    const nut3cham = document.querySelectorAll('div[aria-label="Hành động với bài viết này"]');
    const reels = document.querySelectorAll('a[aria-label="Mở thước phim trong Công cụ xem của Reels"]');
    divContainer.forEach((element) => {
        const containsDivBaiShare = Array.from(divbaishare).some(child => element.contains(child));
        const containsNut3Cham = Array.from(nut3cham).some(child => element.contains(child));
        const containsReels = Array.from(reels).some(child => element.contains(child));
        const hasH3 = "";
         Array.from(divbaishare).some(child => {
            if (element.contains(child)) { 
                const h3 = child.querySelector('h3');
                hasH3 = h3 && h3.parentElement === child; 
            }
            hasH3 = false;
        });
        if ((containsDivBaiShare && containsNut3Cham && hasH3) || (containsNut3Cham && containsReels && hasH3)) {
            const button3Cham = element.querySelector('div[aria-label="Hành động với bài viết này"]');
            if (button3Cham) {
                console.log("Click vào element !");
                button3Cham.click(); 
                return; 
            }
        }
    });
    setTimeout(() => {
        const elements = document.querySelectorAll('div.x1ey2m1c.xds687c.x17qophe.xg01cxk.x47corl.x10l6tqk.x13vifvy.x1ebt8du.x19991ni.x1dhq9h.x9jk4nr.x10vv0rk.x1mn05ot.x4u6ece');
        console.log("Số element:", elements.length);
        if (elements.length > 0) {
            const lastElement = elements[elements.length - 1];
            lastElement.click();
        } else {
            console.log("Không tìm thấy phần tử");
        }
    }, 3000);
    setTimeout(() => {
        console.log("done");
        const elements = document.querySelector('div[aria-label="Chuyển"]');
        if (elements) {
            elements.click();
        } else {
            console.log("không thấy nút chuyển");
        }
    }, 3000);
    window.scrollBy(0, 50);
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        console.log("Đã cuộn đến cuối trang");
    }

}, 2000);
