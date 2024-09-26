function Card_clicked(event) {
    const card = event.currentTarget;
    const Id = card.getAttribute('data-Id')
    var title = card.getAttribute('data-title')

    title = title.replace(/ /g, '-')
    window.location.href = `/home/movie/${title}/${Id}`;

}