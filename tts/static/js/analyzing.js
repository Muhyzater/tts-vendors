const AnalyzeBtn = $('#btn-send')
const Input_text = $('#input-text')
const useTaskeel = $('#useTashkeel')

const Salma = $('#salma')
const Azure = $('#azure')
const Google = $('#google')



function onAnalyzeClick(root_path) {
    get_results(root_path)
}

function setSample(sample) {
    Input_text.val(sample)
    onTextChange()
}

function onTextChange() {
    if (Input_text.val().trim().length > 0) {
        AnalyzeBtn.prop('disabled', false)
    } else {
        AnalyzeBtn.prop('disabled', true)
    }
}

function get_results(root_path) {
    text = Input_text.val()
    tashkeel = useTaskeel.is(':checked')
    encoding = 'mp3'

    get_vendor_result(root_path, text, 'salmaai', encoding, tashkeel, Salma)
    get_vendor_result(root_path, text, 'microsoft', encoding, tashkeel, Azure)
    get_vendor_result(root_path, text, 'google', encoding, tashkeel, Google)

}

function handle_success(response, vendor) {

    player = vendor.find('.audio > audio')[0]
    source = vendor.find('.audio > audio > source')[0]

    source.src = URL.createObjectURL(new Blob([response]))
    player.load()

    vendor.find('.audio').prop('hidden', false)
    vendor.find('.filler').prop('hidden', true)
}

function handle_failure(vendor) {
    vendor.find('.audio').prop('hidden', true)
    vendor.find('.filler').prop('hidden', false)

}

function get_vendor_result(root_path, text, vendor_str, encoding, tashkeel, vendor) {

    vendor.find('.audio').prop('hidden', true)
    vendor.find('.filler').prop('hidden', true)

    xhr = new XMLHttpRequest()
    xhr.open('POST', `${root_path}/tts`)
    xhr.responseType = 'blob'
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    xhr.onreadystatechange = function () {
        if (this.status == 200) {
            handle_success(this.response, vendor)
        } else {
            handle_failure(vendor)
        }
    }

    xhr.send(JSON.stringify({
        text: text,
        vendor: vendor_str,
        encoding: encoding,
        tashkeel: tashkeel
    }))
}