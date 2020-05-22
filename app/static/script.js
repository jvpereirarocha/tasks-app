const links = document.querySelectorAll('.removeLink')
const baseUrl = 'http://localhost:5000'

if (links !== null) {

    console.log(links.length)

    links.forEach((element) => {
        element.onclick = (e) => {

            const message = confirm('Are you sure to delete this task?')

            if (message == true) {

                const getName = element.getAttribute('name')
                const id = getName.split('-')[2]
                fetch(`${baseUrl}/tasks/delete/${id}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                })
                .catch((error) => {
                    console.log(error)
                })
            }

            setInterval(() => {

                window.location.replace(`${baseUrl}/tasks`)

            }, 1000)

        }
    })
}
