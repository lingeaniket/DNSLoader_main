function onSubmit(){fetch("https://api.ipify.org?format=json").then((response)=>response.json()).then((data)=>{const ip=data.ip;fetch(`/whatis-my-ip-data?ip=${ip}`).then((response)=>response.json()).then((data)=>{const whatismyipdata=document.getElementById("whatismyipdata");result=data;whatismyipdata.innerHTML=`
    <section class="about">
        <div class="container" data-aos="fade-up">
            <div class="row gx-0">
                <div class="col-lg-12 d-flex flex-column justify-content-center" data-aos="fade-up" data-aos-delay="200">
                    <div class="content justify-content-center text-center">
                        <p>My Public IPv4:<b>${result.ipv4}</b></p>
                        <p>My Public IPv6:<b>Not Detected</b></p>
                        <p>My ISP:<b>${result.address.org}</b></p>
                        <p>
                            My Location:<b>${result.address.city}, ${result.address.state}, ${result.address.country}</b>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>`})})}
function onload(){document.getElementById("loader").style.display="block";onSubmit()}