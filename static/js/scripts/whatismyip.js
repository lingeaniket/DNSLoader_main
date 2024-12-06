function onSubmit() {
    fetch("https://api.ipify.org?format=json").then((response) => response.json()).then((data) => {
        const ip = data.ip; fetch(`/whatis-my-ip-data?ip=${ip}`).then((response) => response.json()).then((data) => {
            const whatismyipdata = document.getElementById("whatismyipdata"); result = data; whatismyipdata.innerHTML = `
    <section class="about">
        <div class="container" data-aos="fade-up">
            <div class="row gx-0">
                <div class="col-lg-12 d-flex flex-column justify-content-center " data-aos="fade-up" data-aos-delay="200">
                    <div class="content d-flex flex-wrap fs-6 justify-content-center text-center">
                        <div class="w-100 p-2">My Public IPv4:<b>${result.ipv4}</b></div>
                        <div class="w-100 p-2">My Public IPv6:<b>Not Detected</b></div>
                        <div class="w-100 p-2">My ISP:<b>${result.address.org}</b></div>
                        <div class="w-100">
                            My Location:<b>${result.address.city}, ${result.address.state}, ${result.address.country}</b>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>`})
    })
}
function onload() { document.getElementById("loader").style.display = "block"; onSubmit() }