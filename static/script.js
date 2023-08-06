AWS.config.update({
  region: "us-west-2",
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: "us-west-2:2ec3a334-001d-470f-ade9-4a39be853627",
  }),
});

const html_form = document.querySelector("form");
const btn = document.querySelector("button");
html_form.addEventListener("submit", (e) => {
  e.preventDefault();
  image_input_selector = "#image_file";
  email_input_selector = ".email-input";
  bucket_name =
    "c82801a1763196l4500304t1w747434-lambdalayerbucket-u6v8gr4uvj7p";
  const files = document.querySelector("#image_file").files;
  if (files) {
    let file = files[0];
    let fileName = file.name.replaceAll(" ", "-");
    btn.innerText = "Uploading File, Please Wait..";

    let user_input_values = document.querySelectorAll(email_input_selector);
    user_input_values = [...user_input_values];
    let emails = user_input_values
      .map((emailInput) => emailInput.value.trim())
      .filter((email) => email !== "");

    let S3_Upload = new AWS.S3.ManagedUpload({
      params: {
        Bucket: bucket_name,
        Key: fileName,
        Body: file,
        Metadata: {
          recipients: emails.join(","),
        },
      },
    });

    let promise = S3_Upload.promise();

    promise.then(
      function (response) {
        html_form.reset();
        alert("The File has been Successfully Uploaded");
        btn.innerText = "Upload the File";
      },
      function (err) {
        return alert("Error While Uploading.", err.message);
      }
    );
  }
});
