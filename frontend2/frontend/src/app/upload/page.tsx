'use client';

import { useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useDropzone } from "react-dropzone"

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFile(acceptedFiles[0])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "text/csv": [".csv"],
    },
    multiple: false,
  })

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault()
    if (!file) {
      setMessage("Por favor, selecione um arquivo.")
      return
    }

    setIsLoading(true)
    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      })

      if (response.ok) {
        setMessage("Arquivo processado com sucesso!")
        setTimeout(() => router.push("/"), 2000)
      } else {
        const data = await response.json()
        setMessage(data.error || "Erro ao processar o arquivo.")
      }
    } catch (error) {
      setMessage("Erro ao enviar o arquivo.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">Upload de Arquivo CSV</h2>
          <form onSubmit={handleSubmit}>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition duration-300 ease-in-out ${
                isDragActive ? "border-blue-400 bg-blue-50" : "border-gray-300 hover:border-blue-400 hover:bg-blue-50"
              }`}
            >
              <input {...getInputProps()} />
              {file ? (
                <p className="text-sm text-gray-600">Arquivo selecionado: {file.name}</p>
              ) : isDragActive ? (
                <p className="text-sm text-blue-500">Solte o arquivo aqui...</p>
              ) : (
                <p className="text-sm text-gray-500">Arraste e solte um arquivo CSV aqui, ou clique para selecionar</p>
              )}
            </div>
            <button
              type="submit"
              className={`mt-6 w-full py-3 px-4 rounded-lg text-white font-semibold transition duration-300 ease-in-out ${
                isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"
              }`}
              disabled={isLoading}
            >
              {isLoading ? "Processando..." : "Enviar Arquivo"}
            </button>
          </form>
          {message && (
            <p className={`mt-4 text-center ${message.includes("sucesso") ? "text-green-600" : "text-red-600"}`}>
              {message}
            </p>
          )}
        </div>
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
          <Link
            href="/"
            className="block w-full text-center py-2 px-4 rounded-lg text-blue-500 font-semibold hover:bg-blue-50 transition duration-300 ease-in-out"
          >
            Voltar para o Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}