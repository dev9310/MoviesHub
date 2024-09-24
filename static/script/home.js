function Card_clicked(event) {
    const card = event.currentTarget;
    const index = card.getAttribute('data-index')
    console.log(index)
    window.location.href = `/home/movie=${index}`;

}