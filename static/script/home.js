function Card_clicked(event) {
    const card = event.currentTarget;
    const index = card.getAttribute('data-index')
    var title = card.getAttribute('data-title')
    title = title.replace(/ /g, '-')
    window.location.href = `/home/movie/${title}${index}`;

}