$(document).ready(function () {
    $('.slick-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true
    });

    $('#change-product-btn').on('click', function () {
        var slideCount = $('.slick-slider .slick-slide').length;
        var randomSlide = Math.floor(Math.random() * slideCount);
        $('.slick-slider').slick('slickGoTo', randomSlide);
    });

});


$(document).ready(function() {
    let totalForms = parseInt($('#id_form-TOTAL_FORMS').val()); // Get the initial total forms count

    $('#add-more-images').click(function() {
        const newImageForm = $('.image-form:last').clone(true); // Clone the last image form
        newImageForm.find('input').val(''); // Clear input values in the new form
        newImageForm.find('label').each(function() {
            const htmlFor = $(this).attr('for');
            if (htmlFor) {
                const parts = htmlFor.split('-');
                parts.splice(-2, 1, totalForms); // Update the 'for' attribute with the new form index
                const newFor = parts.join('-');
                $(this).attr('for', newFor);
            }
        });
        totalForms++; // Increment the total forms count
        $('.image-forms').append(newImageForm); // Append the new image form
    });
});


// Vanilla JavaScript code
document.addEventListener('DOMContentLoaded', function () {
    const slider = document.getElementById('slider');
    const list = document.getElementById('list');
    const switchListBtn = document.getElementById('switch-view-list-btn');
    const switchSliderBtn = document.getElementById('switch-view-slider-btn');
    const randomBtn = document.getElementById('change-product-btn');

    switchListBtn.addEventListener('click', function () {
        if (list.style.display === 'none') {
            slider.style.display = 'none';
            randomBtn.style.display = 'none';
            switchListBtn.style.backgroundColor = 'rgb(102, 0, 102)';
            switchSliderBtn.style.backgroundColor = 'white';
            list.style.display = 'flex';
        }
    });

    switchSliderBtn.addEventListener('click', function () {
        if (slider.style.display === 'none') {
            slider.style.display = 'block';
            randomBtn.style.display = 'block';
            switchSliderBtn.style.backgroundColor = 'rgb(102, 0, 102)';
            switchListBtn.style.backgroundColor = 'white';
            list.style.display = 'none';
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.querySelector('select[name="category"]');
    const measurementsDiv = document.getElementById('measurements');
    const bottomMeasurementsDiv = measurementsDiv.querySelector('.bottom_measurements');
    const topMeasurementsDiv = measurementsDiv.querySelector('.top_measurements');

    const sellButton = document.getElementById('sell');
    const auctionButton = document.getElementById('auction');
    const auctionFields = document.getElementById('auction_fields');
    const priceField = document.getElementById('price_field');
    const auctionTypeField = document.getElementById('auction_type');

    // Category script
    if (categoryField && measurementsDiv && bottomMeasurementsDiv && topMeasurementsDiv) {
        bottomMeasurementsDiv.style.display = 'none';
        topMeasurementsDiv.style.display = 'none';

        categoryField.addEventListener('change', function () {
            bottomMeasurementsDiv.style.display = 'none';
            topMeasurementsDiv.style.display = 'none';

            switch (categoryField.value) {
                case 'Pants':
                    measurementsDiv.style.display = 'block';
                    bottomMeasurementsDiv.style.display = 'block';
                    break;
                case 'Jacket':
                case 'Sweatshirts & Hoodies':
                case 'Polo':
                    measurementsDiv.style.display = 'block';
                    topMeasurementsDiv.style.display = 'block';
                    break;
                default:
                    measurementsDiv.style.display = 'none';
                    break;
            }
        });

        categoryField.dispatchEvent(new Event('change'));
    }

    // Auction/Sell script
    if (sellButton && auctionButton && auctionFields && priceField && auctionTypeField) {
        auctionFields.style.display = 'none';
        priceField.style.display = 'block';

        sellButton.addEventListener('click', function () {
            auctionFields.style.display = 'none';
            priceField.style.display = 'block';
            sellButton.style.backgroundColor = 'rgb(102, 0, 102)';
            auctionButton.style.backgroundColor = 'white';
            auctionTypeField.value = 'sell';
        });

        auctionButton.addEventListener('click', function () {
            auctionFields.style.display = 'block';
            priceField.style.display = 'block';
            auctionButton.style.backgroundColor = 'rgb(102, 0, 102)';
            sellButton.style.backgroundColor = 'white';
            auctionTypeField.value = 'auction';
        });
    }
});


